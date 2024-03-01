

from fastapi import HTTPException, status


sql_exeption = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Inernal server error")