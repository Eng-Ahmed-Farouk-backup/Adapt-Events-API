# Adapt-Events-API
a project made with python FastAPI and sqlite3 for databse to show teenagers non-profit events like Adapt community
<img width="737" height="526" alt="image" src="https://github.com/user-attachments/assets/4c301590-627a-4955-821e-a0ee6b85669c" />

## CAUTION
you have to be toooooooooooooo pro to see this project because this project is the most one hour high quality project in the universe

## How to use
### whole docs page
this page contains all functions that this API can perform (only use if you are a pro)

https://teenagers-events-production.up.railway.app/docs

### get events
use this link to see the current events:

https://teenagers-events-production.up.railway.app/

you can also specify events by thier id,name,country,city,tags and even the date (specifying the date gives you events that are after that date)

https://teenagers-events-production.up.railway.app/?city=alexandria

this is an example of how to specify city
### produce API key
you can use this link to make an api key using a post request that only asks for your daily limit

https://teenagers-events-production.up.railway.app/generate_api_key

if you are a pro use the docs links and generate it from there
### add new event
use this link with a post request that contains the name,description,tags,date,city,country and ticket price of the event

https://teenagers-events-production.up.railway.app/add_event?api_key=api_key

make sure to replace the placeholder "api_key" with your API key

also in the post request make sure that the date is formatted in this format 

%y-%m-%d i.e 2026-11-15

also any event added will be removed if its date has already passed for example if today is 2026-01-01 and you type the date of the event 2025-31-12 it will be automatically removed

or just use the docs page if you are a pro
### delete an event
use this link to delete an existing event

https://teenagers-events-production.up.railway.app/delete_event?id=id&api_key=api_key

just replace the placeholder id with the id of the event and the placeholder api_key with your api_key

# Author
this is an API Made By Ahmed Farouk Passionate about STEAM, Entrepreneurship

- Leader of Innovations Hack Club
- Founder & CEO of Adapt Community
- Ex Contractor @ Hack club under the Management of Christina (the co founder)

