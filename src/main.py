from fastapi import FastAPI
from src.database import async_session_maker, async_engine, engine
from sqlalchemy import select
from src.auth.models import posts, users

app = FastAPI(

)




@app.get("/")
def get_smth():
     




@app.on_event("startup")
async def startup():
    async with async_engine.connect() as conn:
        res = conn.exe

#
# @app.on_event("shutdown")
# async def shutdown():
#     await engine.commit()

# @app.get("/")
# async def read_root():
#     query = (
#         select(
#             posts.user_table.c.id,
#             posts.user_table.c.created_at,
#             posts.user_table.c.title,
#             posts.user_table.c.content,
#             posts.user_table.c.user_id,
#             posts.user_table.c.name.label("username"),
#         )
#         .select_from(posts.posts_table.join(users.user_table))
#         .order_by(posts.posts_table.c.created_at)
#     )
#     result = await engine.execute(query)
#     return result.all()
