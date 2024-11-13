#這段程式碼的目的是建立一個基於 FastAPI 的簡單 Web 應用程式，讓用戶可以透過瀏覽器或 API 工具請求資料。
from fastapi import FastAPI #導入 FastAPI 庫，用來建立 Web API。
from models import Todo

app = FastAPI() #建立一個 FastAPI 應用程式的實例。


@app.get("/") #設定一個根路徑 / 的 GET 請求處理函數 root()，當訪問這個路徑時會執行此函數。
async def root(): #FastAPI 使用 ASGI（Asynchronous Server Gateway Interface），可以進行異步處理，允許同時處理多個請求，適合需要高效處理 I/O 的應用程式。
    return {"message": "Hello World"} #函數 root() 回傳一個簡單的 JSON 資料 {"message": "Hello World"}。

#uvicorn main:app --reload 是用來啟動 FastAPI 應用程式的命令。這裡：
#uvicorn 是 ASGI 伺服器，可以有效率地處理異步請求。
#main:app 指的是應用程式所在的檔案和物件名稱（在 main.py 檔案裡的 app）。
#--reload 則啟用自動重新加載模式，讓伺服器在偵測到程式碼變更時自動重新啟動，方便開發測試。


todos = []
#Getalltodos
@app.get("/todos")
async def get_todos(): 
    return {"todos": todos}

#Get single todo
#saving a list we can write it to a database, and add database functionality next(將待辦事項存儲在列表中是一個簡單的做法，當你的應用程式需要處理更多數據、提供持久化存儲時，將資料從列表寫入資料庫是很自然的進步。這樣可以確保待辦事項在應用程式重啟或關閉後不會丟失，並且可以更高效地管理大規模數據。)
#todo_id 來自 URL 路徑，會傳遞給函數作為參數。
#這個函數的作用是根據傳入的 todo_id 查找 todos 列表中的待辦事項。如果找到了匹配的待辦事項，則返回該待辦事項；如果找不到，則返回一條訊息告訴用戶沒有找到該待辦事項。
@app.get("/todos/{todo_id}") #表示當接收到 GET 請求時，將會調用下面定義的函數來處理這個請求。(@app.get("/todos/{todo_id}") 是 FastAPI 中的路由裝飾器，表示當發送 GET 請求到 /todos/{todo_id} 路徑時，會觸發相應的函數處理請求，並可以從 URL 中提取 todo_id 參數來進行處理。)
async def get_todo(todo_id: int):  #todo_id: int這是函數的參數，要求傳入一個整數類型的 todo_id，代表待辦事項的唯一標識符。
    for todo in todos: #這行開始了一個循環，遍歷 todos 這個變量。假設 todos 是一個包含多個待辦事項（可能是物件或字典）的列表。這裡會逐個檢查每個 todo
        if todo.id == todo_id: #這行檢查當前迭代的 todo 是否與傳入的 todo_id 匹配。假設每個 todo 物件有一個 id 屬性，這行檢查其是否等於傳入的 todo_id
            return {"todo":todo} #如果找到了匹配的 todo，則返回一個字典，字典中包含匹配的 todo。這會將該 todo 物件包裝在 {"todo": todo} 格式中作為回應。
    return {"message": "No todos found"} #如果在循環結束後，仍然沒有找到匹配的 todo，則返回一個包含訊息的字典 {"message": "No todos found"}，提示用戶沒有找到相應的待辦事項

#Create a todo
#這段程式碼定義了一個處理 POST 請求的函式 create_todos，用來接收請求中的資料（todo）並將其加入 todos 列表中。函式會回傳一個包含訊息 "Todo has been added" 的 JSON 回應，表示新的待辦事項已成功加入。


@app.post("/todos") #告訴 FastAPI 當收到 POST 請求時，並且請求路徑為 /todos，會觸發 create_todos 函式。
async def create_todos(todo:Todo): #?定義一個異步函式 create_todos，並且參數 todo 會從請求的內容中解析出來，符合 Todo 類別。（todo 是用來接收傳遞到函數的資料，並且這些資料會被轉換為符合 Todo 類別的物件。)
    todos.append(todo) #?將接收到的 todo 物件加入 todos 列表。(todos.append(todo) 是將這些資料加入到 todos 列表。)
    return {"message": "Todo has been added"}#回傳一個 JSON 格式的回應，告訴用戶待辦事項已成功新增。

#在 Postman 中發送 POST 請求時，通常需要在「Body」中包含數據，因為 POST 請求是用來創建或提交數據的。這些數據會被包含在請求的主體中，而非像 GET 請求那樣直接附加在 URL 中。你可以選擇不同的格式（如 JSON、x-www-form-urlencoded 或 form-data）來提交這些數據，這樣伺服器就能夠處理和存儲這些資料。
#在 Postman 中，按下 "Send" 按鈕會向伺服器發送一個 HTTP 請求。當你選擇 POST 請求時，Postman 會將你在 Body 部分輸入的資料發送到伺服器，並請求伺服器處理這些資料。伺服器收到資料後，通常會根據請求的內容進行處理（如新增資料、更新資料等），然後返回相應的回應（如成功訊息或錯誤訊息）。

#Update a todo
#這個 PUT 請求處理函數讓用戶可以更新指定的待辦事項，這樣的代碼可以有效地實現列表中待辦事項的更新功能
@app.put("/todos/{todo_id}") #@app.put("/todos/{todo_id}"): 這是 FastAPI 中的路由裝飾器，當接收到針對 /todos/{todo_id} 路徑的 PUT 請求時，會觸發下方的 update_todo 函數。todo_id 是路徑參數，表示要更新的待辦事項 ID。
async def update_todo(todo_id: int, todo_obj: Todo):  
#async def update_todo(todo_id: int, todo_obj: Todo):: 這是 update_todo 函數的定義。它是一個異步函數，接收兩個參數：
#todo_id: 整數類型的待辦事項 ID，用於識別要更新的待辦項目。
#todo_obj: 一個 Todo 類型的物件，包含新的待辦事項數據，作為更新內容。 
    for todo in todos:  #for todo in todos:: 這行開始了一個循環，遍歷 todos 列表中的每一個待辦事項，以尋找與 todo_id 匹配的項目。
        if todo.id == todo_id:  #if todo.id == todo_id:: 檢查當前的 todo 是否與 todo_id 匹配。如果相符，說明找到需要更新的待辦事項。
            todo.id = todo_id #todo.id = todo_id: 這行是多餘的，因為 todo.id 已經與 todo_id 相符，且 ID 通常不應在更新時被改變。可以刪除此行。
            todo.item = todo_obj.item #todo.item = todo_obj.item: 將 todo.item 更新為 todo_obj.item，將新的待辦事項內容賦值給現有的 todo。
            return {"todo":todo}  #return {"todo": todo}: 如果找到並更新了待辦事項，則回傳更新後的 todo，並以字典形式包裝為 {"todo": todo}。
    return {"message": "No todos found to update"}


#Delete a todo
#這個 delete_todo 函數的作用是從 todos 列表中刪除指定 todo_id 的待辦事項。如果成功找到並刪除該待辦事項，就返回一條成功的消息；如果沒有找到該待辦事項，就返回一條錯誤訊息。
@app.delete("/todos/{todo_id}") #這是 FastAPI 中的一個路由裝飾器，定義了一個處理 HTTP DELETE 請求的路由。這個路由會觸發 delete_todo 函數，並且 URL 中的 {todo_id} 會作為路徑參數傳遞給該函數。
async def delete_todo(todo_id: int):   #async def delete_todo(todo_id: int): 這定義了一個異步函數 delete_todo，該函數接受一個整數類型的參數 todo_id，用來標識待辦事項。這個函數會處理刪除指定待辦事項的邏輯。
    for todo in todos: #for todo in todos:: 這行啟動了一個循環，遍歷 todos 這個列表。假設 todos 是包含多個待辦事項的列表，這裡會檢查每個 todo 物件。
        if todo.id == todo_id: 
            todos.remove(todo) #todos.remove(todo): 當找到匹配的待辦事項後，這行將會從 todos 列表中移除該 todo 物件。這樣就完成了待辦事項的刪除。
            return {"message":"Todo has been DELETED!"}  #刪除操作成功後，返回一個字典，並附帶消息 "Todo has been DELETED!"，告訴用戶該待辦事項已經成功刪除。
    return {"message": "No todos found"}

@app.put("/")
async def put():
    return {"message": "hello from the put route"}