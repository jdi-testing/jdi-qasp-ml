// Collect features from a web-page
// Generate global unique identifier
function gen_uuid(e) {
  if (e['uuid'] == undefined) {
     //e['uuid'] = btoa(Math.random()) + btoa(Date.now());
     e['uuid'] = Math.random().toString().substring(2,12) + Date.now().toString().substring(5) + Math.random().toString().substring(2,12);
     return e;
  } else {
     return e;
  }
}

function collect_attributes(el) {
   var items = {}; 
   for (index = 0; index < el.attributes.length; ++index) { 
      items[el.attributes[index].name] = el.attributes[index].value 
   }; 
   return items;
}

// Assing uuid to all elements
[...document.querySelectorAll('*')].forEach(el => {
   gen_uuid(el)
})

// generate tree representation
treeDataset = [...document.querySelectorAll('*')].map(el => {
   _x = el.getBoundingClientRect()['x'],
   _y = el.getBoundingClientRect()['y'],
   _width = el.getBoundingClientRect()['width'],
   _height = el.getBoundingClientRect()['height']
   _displayed = (_x<0) | (_y<0) | (_width<=1) | (_height<=1)

   return {
     tag_name: el.tagName,
     element_id: el.uuid,
     parent_id: (el.parentElement == null) ? null : el.parentElement.uuid,
     x: _x,
     y: _y,
     width: _width,
     height: _height,
     displayed: !_displayed,
     onmouseover: el.onmouseover,
     onmouseenter: el.onmouseenter,
     attributes: collect_attributes(el),
     text: el.innerText,
     style: window.getComputedStyle(el)
   }
})

return treeDataset;
