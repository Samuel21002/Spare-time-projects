    const toDo_textbox = document.getElementById('toDo_textbox')  //Textvox
    var output = document.getElementById('list_Output') //Displays messages
    var toDo_ul = document.getElementById('toDo_List')  //List element
    let editMode = false  //Changes if user edits the toDo-items

    var list_elems = []
    var id = 1  //Just for creating element "id's" for the markup 

    //Gets all elements from the cache if there is any
   

      const str = localStorage.getItem('array_elems')

      list_elems = JSON.parse(str)
      console.log(`List length : ${list_elems.length}`)
      console.log('The page is fully loaded.')

      list_elems.forEach((f) => createObjectToView(f))  //Creates the <li> -elements for the page
    

    //Prevents the submit functionality
    function handleSubmit(event) {
      event.preventDefault()
      return 0
    }

    //For adding items when user presses enter (if textbox is selected)
    function validateEnterKeyPress(event) {
      if (event.keyCode == 13) {
        console.log('Enter key is pressed')
        add_toDo(toDo_textbox.value)
      } else {
        return false
      }
    }

    //For drawing the <li> -items
    function createObjectToView(item) {
      let li_elem = document.createElement('li')
      li_elem.className = 'toDo_item'
      li_elem.id = `toDo_item_${id}`

      let item_inputbox = document.createElement('input')
      item_inputbox.className = 'toDo_item_textBox'
      item_inputbox.value = item

      item_inputbox.setAttribute('readOnly', 'readOnly')

      let item_editButton = document.createElement('button')
      item_editButton.className = 'toDo_item_button'
      item_editButton.innerText = 'Edit'
      id++ // Increments on add
      var index = list_elems.indexOf(item_inputbox.value)

      //Edit item button (click)
      item_editButton.addEventListener('click', () => {

        //If 'editMode' value is false, set it to true and autofocus on the list element textbox
        if (!editMode) {
          item_inputbox.setAttribute('readonly', false)
          item_inputbox.removeAttribute('readonly')
          item_inputbox.style = 'font-style: underline' //ADD LATER!!
          item_inputbox.focus()
          item_editButton.innerText = 'Save Changes'
          editMode = true
        } else {

          //Set 'editMode' to false upon change
          item_inputbox.setAttribute('readonly', 'readonly')
          item_editButton.innerText = 'Edit'
          list_elems[index] = item_inputbox.value

          editMode = false
        }
      })

      //Edit item (via pressing enter)
      item_inputbox.addEventListener('keydown', (e) => {
        if (editMode && event.keyCode == 13) {
          item_inputbox.setAttribute('readonly', 'readonly')
          item_editButton.innerText = 'Edit'
          list_element = item_inputbox.value
          list_elems[index] = item_inputbox.value

          editMode = false
        }
      })

      // Delete button
      let item_deleteButton = document.createElement('button')
      item_deleteButton.id = `toDo_delete_${li_elem.id}`
      item_deleteButton.className = 'toDo_item_button'
      item_deleteButton.innerText = 'Delete'

      //Deleting Item
      item_deleteButton.addEventListener('click', () => {
        toDo_ul.removeChild(li_elem)
        output.innerText = 'Item deleted!'
        let index = list_elems.indexOf(item_inputbox.value)
        if (index > -1) {
          list_elems.splice(index, 1)
          console.log("Item Deleted!")
        }
        console.log(list_elems)
      })

      li_elem.appendChild(item_inputbox)
      li_elem.appendChild(item_editButton)
      li_elem.appendChild(item_deleteButton)
      toDo_ul.appendChild(li_elem)
    }

    //Prompts the user before delete. Clear the cache and all <li> -elements
    function clearAll(event) {
      list_elems.splice(0, list_elems.length)

      const myNode = document.getElementById('toDo_List')
      const response = confirm('Are you sure you want to do that?')

      if (response) {
        while (myNode.firstChild) {
          myNode.removeChild(myNode.lastChild)
          output.innerText = 'List cleared from cache!'
        }
        saveToJSON()
      }
    }

    //Checks if the item is already in the list, then draws it.
    function add_toDo(obj) {
      if (obj) {
        list_elems.push(obj)

        output.innerHTML = 'Item added to list!'
        console.log('Item added to list!')
        createObjectToView(obj)
      } else if (list_elems.some((value) => value === obj)) {
        output.innerText = 'Item Already Exists!'
        console.log('Item already exists!')
      } else {
        output.innerText = 'Cannot add item!'
      }
    }

    window.onbeforeunload = saveToJSON
    function saveToJSON() {
      const jsonArr = JSON.stringify(list_elems)

      //Save toDo-list to localStorage -cache
      try {
        localStorage.setItem('array_elems', jsonArr)
        console.log('Saving items to localstorage')
      } catch (e) {
        if (e == QUOTA_EXCEEDED_ERR) {
          alert('Cache is full! Try deleting a few items or try again!')
        }
      }
    }
