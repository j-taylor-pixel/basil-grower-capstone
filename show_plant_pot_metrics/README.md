# show_plant_pot_metrics

cd backend
flask run
or
docker build . -t show
docker run -p 5000:5000 show

``
# todo 
db:
fill with dummy data tick

logic:
read influx db tick
assume all influx db values are between 0%-100%  tick
aggregration type? probably do most recent? tick
dynamically update frontend: do
serve json
create json endpoint so plant pot can write to the database without database query app


frontend:
chose frontend: 
display color coded tiles with number on it 
label on tiles to selected metric


