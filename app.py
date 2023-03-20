import requests
from flask import Flask, render_template, request

app = Flask(__name__)

URL = 'https://bmapiproject.herokuapp.com/api/v1/30908139127022/classifydata'

resources_available_mapper = {
    "Rear-end collisions": "1 emergency responders, 2 supplies, 0 boats",
    "Head-on collisions": "8 emergency responders, 6 supplies, 3 boats",
    "Side-impact collisions": "4 emergency responders, 9 supplies, 2 boats",
    "T-bone collisions": "8 emergency responders, 1 supplies, 4 boats",
    "Multi-car pileups": "3 emergency responders, 5 supplies, 0 boats",
    "Single-car accidents": "7 emergency responders, 0 supplies, 7 boats",
    "Hit and run accidents": "8 emergency responders, 3 supplies, 8 boats",
    "Pedestrian accidents": "3 emergency responders, 2 supplies, 7 boats"
}

distribution_of_aid_mapper = {
    "Rear-end collisions": "Food, shelter",
    "Head-on collisions": "water",
    "Side-impact collisions": "Food, water, shelter",
    "T-bone collisions": " shelter",
    "Multi-car pileups": " water, shelter",
    "Single-car accidents": "Food, water",
    "Hit and run accidents": "water, shelter",
    "Pedestrian accidents": "Food, water, shelter"
}

response_time_mapper = {
    "Rear-end collisions": "2",
    "Head-on collisions": "3",
    "Side-impact collisions": "5",
    "T-bone collisions": "6",
    "Multi-car pileups": "1",
    "Single-car accidents": "0.5",
    "Hit and run accidents": "2",
    "Pedestrian accidents": "4"
}


@app.route('/')
def index():
    desc = request.form.get("desc")
    return render_template('index.html', action_plan="None", desc="")


@app.route('/generateactionplan', methods=['POST'])
def generateactionplan():
    desc = request.form.get("desc")

    if desc != None:
        # sending get request and saving the response as response object
        PARAMS = {'data': desc}
        r = requests.post(url=URL, json=PARAMS)
        categories = []
        if r.status_code == 200:
            return_data = r.json()
            for k, v in return_data.items():
                categories.append(v)

        # Build action plan
        for i in range(len(categories)):
            resources_avilable = resources_available_mapper[categories[i]]
            distribution_of_aid = distribution_of_aid_mapper[categories[i]]
            response_time = response_time_mapper[categories[i]]
            plan_name = categories[i]

    return render_template('index.html', action_plan="exist", desc=desc, resources_avilable=resources_avilable,
                           distribution_of_aid=distribution_of_aid, response_time=response_time, plan_name=plan_name)


if __name__ == '__main__':
    app.run()
