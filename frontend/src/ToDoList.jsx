import { useState, useEffect, useRef } from "react"

function ToDoList() {
    const [lists, setLists] = useState([])
    const [activeListId, setActiveListId] = useState(1)
    const [items, setItems] = useState([])
    const [newItem, setNewItem] = useState("")
    const [showCompleted, setShowCompleted] = useState(false)
    const removeTimersRef = useRef(new Map())

     useEffect(() => {
        const fetchLists = async () => {
        try {
            const response = await fetch("/api/lists")
            if (!response.ok) {
                throw new Error("Failed to fetch list")
            }
            const data = await response.json()
            setLists(data)

            if(data.length > 0 && !data.some(l => l.to_do_list_id === activeListId)) {
                setActiveListId(data[0].to_do_list_id)
            }
        } catch (error) {
            console.error(error);
        }
    }
    fetchLists()
    }, [])

useEffect(() => {
  const fetchItems = async () => {
    try {
      const url = showCompleted
        ? `/api/lists/${activeListId}/items?include_completed=true`
        : `/api/lists/${activeListId}/items`

      const response = await fetch(url)
      if (!response.ok) throw new Error("Failed to fetch items")

      const data = await response.json()
      setItems(data)
    } catch (error) {
      console.error(error)
    }
  }

  fetchItems()
}, [activeListId, showCompleted])

useEffect(() => {
    if (showCompleted) {
        for (const timerId of removeTimersRef.current.values()) {
            clearTimeout(timerId)
        }
        removeTimersRef.current.clear()
    }
}, [showCompleted])

    function handleInputChange(e){
        setNewItem(e.target.value);

    }

    async function createNewList() {
        const name = prompt("list name?")
        if (!name) return

        try {
            const response = await fetch(`/api/lists`, {method: "POST"})
            if (!response.ok) {
                throw new Error ("Failed to create list")
            }
            const newList = await response.json()
            setLists(lists => [...lists, newList])
            setActiveListId(newList.to_do_list_id)
        } catch (error) {
            console.error(error);

        }

    }

    async function addItem(){
        if(newItem.trim() === "") return
        try {
            const response = await fetch(`/api/lists/${activeListId}/items`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    description: newItem,
                    is_complete: false
                })
            })
            if (!response.ok) {
                throw new Error("Failed to create item")
            }
            const createdItem = await response.json()
            setItems(items => [...items, createdItem])
            setNewItem("")
        } catch (error) {
            console.error(error);
        }
    }

    async function deleteItem(itemId){
        try {
            const response = await fetch(`/api/lists/${activeListId}/items/${itemId}`, {
                method: "DELETE"
            })
            if (!response.ok) {
                throw new Error("Delete Failed")
            }
            setItems(items =>
                items.filter(item => item.item_id !== itemId)
            )
        } catch (error) {
            console.error(error);

        }
    }

    async function renameActiveList() {
        const current = lists.find(l => l.to_do_list_id === activeListId)
        const name = prompt('New list name?', current?.name || "")
        if (!name) return
        try {
            const response = await fetch(`/api/lists/${activeListId}`, {
                method: "PATCH",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name})
            })
            if (!response.ok) {
                const text = await response.text()
                throw new Error(text || "Failed to rename list")
            }
            const updated = await response.json()
            setLists(ls => ls.map(l => (
                l.to_do_list_id === updated.to_do_list_id ? updated : l
            )))
        } catch (error) {
            console.error(error);

        }

    }

    async function toggleComplete(item) {
        const nextIsComplete = !item.is_complete

        setItems(items =>
            items.map(i =>
                i.item_id === item.item_id ? { ...i, is_complete: nextIsComplete } : i
            )
        )

        try {
            const response = await fetch(`/api/lists/${activeListId}/items/${item.item_id}`, {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    description: item.description,
                    is_complete: nextIsComplete
                })
            })
            if(!response.ok) {
                const text = await response.text()
                throw new Error(text || "update Failed")
            }
            const updatedItem = await response.json()
            setItems(items =>
                items.map(i => (i.item_id === updatedItem.item_id ? updatedItem : i))
            )
            const existing = removeTimersRef.current.get(updatedItem.item_id)
            if (existing) {
                clearTimeout(existing)
                removeTimersRef.current.delete(updatedItem.item_id)
            }

            if (updatedItem.is_complete && !showCompleted) {
                const timerId = setTimeout(() => {
                    setItems(items => items.filter(i => i.item_id !== updatedItem.item_id))
                    removeTimersRef.current.delete(updatedItem.item_id)
                }, 5000)
                removeTimersRef.current.set(updatedItem.item_id, timerId)
            }
        } catch (error) {
            console.error(error)
            setItems(items =>
                items.map(i =>
                    i.item_id === item.item_id ? { ...i, is_complete: item.is_complete } : i
                )
            )

        }
    }

    function moveItemUp(itemId){
        setItems(items => {
            const index = items.findIndex(i => i.item_id === itemId)
            if (index <= 0) return items
            const copy = [...items]
            ;[copy[index - 1], copy[index]] = [copy[index], copy[index - 1]]
            return copy
        })
    }

    function moveItemDown(itemId){
        setItems(items => {
            const index = items.findIndex(i => i.item_id === itemId)
            if (index === -1 || index >= items.length - 1) return items
            const copy = [...items]
            ;[copy[index], copy[index + 1]] = [copy[index + 1], copy[index]]
            return copy
        })
    }

return (
    <div className="to-do-list">
        <h1>
            To-Do-List
            <button
                type="button"
                className={`tag ${showCompleted ? "tag-active" : ""}`}
                onClick={() => setShowCompleted(v => !v)}
            >
                {showCompleted ? "Hide completed" : "Show completed"}
            </button>
        </h1>
        <div>
            <div style={{ display: "flex", gap: "8px", alignItems: "center"}}>
                <label>List:</label>
                <select value={activeListId} onChange={(e) => setActiveListId(Number(e.target.value))}>
                    {lists.map(l => (
                        <option key={l.to_do_list_id} value={l.to_do_list_id}>
                        {l.name}
                        </option>
                    ))}
                </select>
                <button onClick={createNewList}>New List</button>
                <button onClick={renameActiveList}>Rename</button>
            </div>
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
                <li key={item.item_id}>
                    <input type="checkbox"
                    checked={!!item.is_complete}
                    onChange={() => toggleComplete(item)}
                    />
                    <span className="text">{item.description}</span>
                    <button
                        className="delete-button"
                        onClick={() => deleteItem(item.item_id)}>Delete
                    </button>
                    <button
                        className="move-button"
                        onClick={() => moveItemUp(item.item_id)}>Move Up
                    </button>
                    <button
                        className="move-button"
                        onClick={() => moveItemDown(item.item_id)}>Move Down
                    </button>
                </li>
            )}
        </ol>
    </div>
)
}

export default ToDoList
