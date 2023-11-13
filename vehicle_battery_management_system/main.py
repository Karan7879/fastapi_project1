from fastapi import FastAPI
import user,sites,batteries,operations

app = FastAPI()


app.include_router(user.signups)
app.include_router(sites.charginroutes)
app.include_router(batteries.batt)
app.include_router(operations.operations)



