// another person may have been updated the editor string
cnl_slides.setSlideText = function (str) {
  // another person updated
  if(str != cnl_globals.editor.codemirror.doc.getValue()) {
    var curr_cursor = cnl_globals.editor.codemirror.doc.getCursor();
    cnl_globals.editor.codemirror.doc.setValue(str);
    cnl_globals.editor.codemirror.doc.setCursor(curr_cursor);
  }
  // this user updated
  else {
    var diff = cnl_globals.dmp.diff_main(this.curr_slide_text, str, false);
    var patches = cnl_globals.dmp.patch_make(this.curr_slide_text, diff);
    var patch_text = cnl_globals.dmp.patch_toText(patches);
    var pre_hash = cnl_globals.hash(this.curr_slide_text);
    var curr_hash = cnl_globals.hash(str);

    socket.send(JSON.stringify({
      "command": "change_slide",
      "room": room_label,
      "id": this.curr_slide_idx,
      "patch_text": patch_text,
      "pre_hash": pre_hash,
      "curr_hash": curr_hash,
    }));
  }

  this.curr_slide_text = str;
  var out = document.getElementById("out");
  out.innerHTML = cnl_globals.md.render(str);
  $('blockquote').addClass('blockquote');
}

cnl_slides.getNewSlide = function () {
  console.log('add clicked');
  
  socket.send(JSON.stringify({
    "command": "new_slide",
    "room": room_label
  }));
}

// callback when new slide is generated
// overriden version has setSlideIndex() (if new slide is set, automatically send it to it)
cnl_slides.setNewSlide = function (data) {
  var new_idx = data;
  $('#slide_list button').before('<li id="slide_' + new_idx + '" class="list-group-item drawer-menu-item" onclick="cnl_slides.getSlideIndex(' + new_idx + ')">Unnamed slide</li>');
  cnl_slides.getSlideIndex(new_idx);
}

/*
// delete slide with index "idx", then click on adjacent slide
cnl_slides.delSlide = function (idx) {
  // called from modal
  if(typeof idx == 'undefined') {
    idx = this.curr_slide_idx;
  }
  // debug: remove idx from server
  console.log('deleted ' + idx);
  // debug end

  var curr_slide = $('#slide_' + idx);

  if(idx === this.curr_slide_idx) {
    // If more slides, get new one
    if($('li.drawer-menu-item').length === 1) {
      this.getNewSlide();
    }
    // Else, find adjacent slides
    else {
      var next_slide = curr_slide.next();
      if(next_slide.length === 0) {
        next_slide = curr_slide.prev();
      }
      var next_slide_idx = parseInt(next_slide.attr('id').split('_')[1]);
      this.getSlideIndex(next_slide_idx);
    }
  }

  //밑에 다 콜백
  // remove from drawer
  curr_slide.remove();
}
*/

cnl_slides.getDelSlide = function (idx) {
  // called from modal
  if (typeof idx == 'undefined') {
    idx = this.curr_slide_idx;
  }

  var curr_slide = $('#slide_' + idx);

  if (idx === this.curr_slide_idx) {
    // If more slides, get new one
    if($('li.drawer-menu-item').length === 1) {
      this.getNewSlide();
    }
    // Else, find adjacent slides
    else {
      var next_slide = curr_slide.next();
      if(next_slide.length === 0) {
        next_slide = curr_slide.prev();
      }
      var next_slide_idx = parseInt(next_slide.attr('id').split('_')[1]);
      this.getSlideIndex(next_slide_idx);
    }
  }

  socket.send(JSON.stringify({
    "command": "del_slide",
    "id": idx,
    "room": room_label
  }));
}

cnl_slides.setDelSlide = function (data) {
  var curr_slide = $('#slide_' + data);
  curr_slide.remove()
}

/*
// change order of slide with index "idx" to previous of slide with index "next"
// overriden version should have websocket
cnl_slides.changeSlideOrder = function (idx, next) {
  // debug: send idx, next
  console.log(idx + ' and ' + next + ' send to server');
  // debug end
  
  if(next !== 0) {
    $('#slide_' + idx).detach().insertBefore('#slide_' + next);
  }
  else {
    // it is last element
    $('#slide_' + idx).detach().appendTo('#slide_list');
  }
}
*/

cnl_slides.setChangeSlideOrder = function (data) {
  var idx = data.id;
  var next = data.next_id;

  console.log('id : ' + idx + '/ next : ' + next)

  if (next !== 0) {
    $('#slide_' + idx).detach().insertBefore('#slide_' + next);
  }
  else {
    $('#slie_' + idx).detach().appendTo('#slide_list')
  }
}

cnl_slides.getChangeSlideOrder = function (idx, next) {
  console.log('id : ' + idx + '/ next : ' + next)
  socket.send(JSON.stringify({
    "command": "change_slide_order",
    "id": idx,
    "next_id": next,
    "room": room_label
  }));
}

/*
// renaming slide
// overriden version should have websocket & modal consideration
cnl_slides.renameSlide = function (idx, name) {
  // called from modal
  if(typeof idx == 'undefined') {
    var idx = this.curr_slide_idx;
    var name = $('#slide_name_input').val();
    if(!name) name = 'unnamed slide'; // default value
  }

  if(name != $('#slide_' + idx).text()) {
    // debug: send to server
    console.log('slide ' + idx + ' renamed to ' + name);
    // end debug
    $('#slide_' + idx).text(name);
    if(idx === this.curr_slide_idx) {
      $('#markdown_title').text(name);
    }
  }
}*/

cnl_slides.setRenameSlide = function (data) {
  var idx = data.rename_slide;
  var name = data.title;

  $('#slide_' + idx).text(name);
  if(idx == this.curr_slide_idx) {
    $('#markdown_title').text(name);
  }
}

cnl_slides.getRenameSlide = function () {
  var idx = this.curr_slide_idx;
  var name = $('#slide_name_input').val();
  
  socket.send(JSON.stringify({
      "command": "rename_slide_title",
      "title": name,
      "id": idx,
      "room": room_label
    }));
}
