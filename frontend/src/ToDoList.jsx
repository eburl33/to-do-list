import { useState } from "react"

function ToDoList() {
    const [items, setItems] = useState([])
    const [newItem, setNewItem] = useState("")

    function handleInputChange(e){
        setNewItem(e.target.value);

    }
    function addItem(){

        if(newItem.trim() !== ""){
        setItems(t => [...t, newItem])
        setNewItem("");
        }
    }
    function deleteItem(index){
        const updatedItems = items.filter((_, i) => i !== index);
        setItems(updatedItems)
    }
    function moveItemUp(index){
        if(index > 0){
            const updatedItems = [...items];
            [updatedItems[index], updatedItems[index - 1]] =
            [updatedItems[index - 1], updatedItems[index]];
            setItems(updatedItems)
        }
    }
    function moveItemDown(index){
        if(index < items.length - 1){
            const updatedItems = [...items];
            [updatedItems[index], updatedItems[index + 1]] =
            [updatedItems[index + 1], updatedItems[index]];
            setItems(updatedItems)
        }

    }
return (
    <div className="to-do-list">
        <h1>To-Do-List</h1>
        <div>
            <input
                type="text"
                placeholder="Enter an Item..."
                value={newItem}
                onChange={handleInputChange} />
            <button
                className="add-button"
                onClick={addItem} >
                Add Item
            </button>
        </div>
        <ol>
            {items.map((item, index) =>
                <li key={index}>
                    <span className="text">{item}</span>
                    <button
                        className="delete-button"
                        onClick={() => deleteItem(index)}>Delete
                    </button>
                    <button
                        className="move-button"
                        onClick={() => moveItemUp(index)}>Move Up
                    </button>
                    <button
                        className="move-button"
                        onClick={() => moveItemDown(index)}>Move Down
                    </button>
                </li>
            )}
        </ol>
    </div>
)
}

export default ToDoList
