
slide deck 
https://www.canva.com/design/DAGY4C8tCBo/G-c9F_-4NaFxquzQGXPXnw/edit?utm_content=DAGY4C8tCBo&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

demo video
https://drive.google.com/file/d/1DA7e7CbZsNSs-u0nZtbg2ZiIQmADWYoi/view?usp=sharing





docker run --name pgvector-container -e POSTGRES_USER=langchain -e POSTGRES_PASSWORD=langchain -e POSTGRES_DB=langchain -p 6024:5432 -d pgvector/pgvector:pg16


response.data.payload.output


Sample Questions for User Interaction with an Insurance Agent:
"Can you give me the claim status? My claim ID is [ClaimID]."
"Can you tell me about my insurance policy?"
"Can you provide detailed information regarding my insurance policy?"

uvicorn main:app --reload
