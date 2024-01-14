from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
# Response, status, HTTPException all does the same work doing this differently

app = FastAPI()

class Schema_for_Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None 


my_posts = [
    {"title" : "title of post 1", "content" : "content of post 1", "id" : 1},
    {"title" : "title of post 2", "content" : "content of post 2", "id" : 2},
]

def ind_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p 

@app.get("/")
async def root():
    return {"message" : "Hello World I am comming"}

@app.get("/posts")
async def get_posts():
    return {"data" : my_posts}

@app.get("/posts/{id}")
# async def get_single_post(id : int, response : Response):
async def get_single_post(id : int):
    # automatically accept id as int
    print(id)
    print(type(id))
    # Here id will get as str type so I need to convert this as int

    indi_post = ind_post((id))
    if not indi_post :
        # response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"ID {id} is not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"Individual Post" : indi_post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(obj_for_schema_post: Schema_for_Post):
    post_dict = obj_for_schema_post.dict()
    post_dict["id"] = randrange(2, 100000)
    my_posts.append(post_dict)
    return {"data" : post_dict}
    # return {"All data" : my_posts}

def find_index_my_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i 
        
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id : int):
    index = find_index_my_post(id)
    if index == None:
        # If the id doesnt exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id} doesn't exist")
    my_posts.pop(index)
    # return {json} It could send no data and will send error because we are sending the status code 204 in the @app 
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id : int, update_post : Schema_for_Post):
    print(update_post) 
    index = find_index_my_post(id)
    if index == None:
        # If the id doesnt exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id} doesn't exist")
    
    post_dict = update_post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data" : post_dict}


