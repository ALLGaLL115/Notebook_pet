from fastapi import HTTPException, status
from services.utils import filter_none_data
from shemas.note import NoteCreate
from utils.unit_of_work import IUnitOfWork


class NoteService:
    async def create_note(uow:IUnitOfWork, notebook_id: int, note: NoteCreate, token:str):
        data_dict = filter_none_data(note.model_dump())
        
        async with uow:
            try:
                if data_dict is None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty input data")

                user = await uow.users.get_current_user(token)
                note_id = await uow.notes.add_one(data_dict)
                await uow.assotiations_notebook_note().add_one(data={"notebook_id": notebook_id, "note_id": note_id})

                await uow.commit()
                return {"status":200, "detail":f"Note with {note_id} added"}



                


            except HTTPException as e:
                await uow.rollback()
                raise e 


    async def get_notes():
        pass 

    async def update_note():
        pass

    async def delete_note():
        pass 
