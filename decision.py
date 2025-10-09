import ui

# Simulate simple decision making

# Make a 3x3 decision making task
decision_ui = ui.ui()
decision_ui.add_element("e1", 0,0,50,50)
decision_ui.add_element("e2", 75,0,50,50)
decision_ui.add_element("e3", 150,0,50,50)

decision_ui.add_element("e4", 0,75,50,50)
decision_ui.add_element("e5", 75,75,50,50)
decision_ui.add_element("e6", 150,75,50,50)

decision_ui.add_element("e7", 0,150,50,50)
decision_ui.add_element("e8", 75,150,50,50)
decision_ui.add_element("e9", 150,150,50,50)

element_values1 = {
    "e1": -0.3,
    "e2": 0.3,
    "e3": 0.2,
    "e4": 0.3,
    "e5": -0.3,
    "e6": 0.3,
    "e7": -0.2,
    "e8": 0.5,
    "e9": -0.4
    }

element_values2 = {
    "e1": -0.3,
    "e2": -0.2,
    "e3": 0.3,
    "e4": -0.3,
    "e5": -0.2,
    "e6": 0.4,
    "e7": -0.2,
    "e8": -0.3,
    "e9": -0.6
    }

def reset_decision_ui(ui, element_values, color = None):
    for e in ui.elements:
        ui.elements[e].data = element_values[e]
        if not color:
            ui.elements[e].color = "grey"
        elif element_values[e] > 0:
            ui.elements[e].color = "green"
        else:
            ui.elements[e].color = "red"

# reset_decision_ui(decision_ui, element_values2)


def make_decision(ui, element_values):
    start = "e1"
    pluses = 0
    minuses = 0
    searched = [start]
    scanpath = [start]
    # if start == target:
    #     mt_, moved = ui.emma_time(start, eye_loc = start)
    #     return mt_, scanpath

    # "See" the color with fewer entries
    greens = 0
    for e in ui.elements:
        if ui.elements[e].color == "green":
            greens += 1
    if greens >= len(ui.elements)/2:
        top_down = "red"
    elif greens == 0:
        top_down = None
    else:
        top_down = "green"
    #print(top_down)
    mt = 0
    while len(searched) != len(ui.elements):
        # Figure out the next target, which is the one with
        # largest activation, but not inhibited.
        activation = ui.bottom_up_activation(start)

        if top_down:
            top_down_activation = ui.top_down_activation(top_down, eye_loc = start)
            for e in top_down_activation:
                if e in activation:
                    activation[e] += top_down_activation[e]

        for e in searched:
            if e in activation:
                del activation[e]

        new_target = max(activation.items(), key=lambda x: x[1])[0]

        mt_, moved = ui.emma_time(new_target, eye_loc = start)
        mt += mt_
        #print(start, new_target, moved, mt)
        if moved: scanpath.append(new_target)

        searched.append(new_target)

        if element_values[new_target] > 0:
            pluses += 1
            #print("found plus")
        if element_values[new_target] <= 0:
            #print("found minus")
            minuses += 1
        if pluses >= len(ui.elements)/2 or minuses >= len(ui.elements)/2:
            break

        if top_down:
            unfound = 0
            for e in activation:
                if e != new_target and ui.elements[e].color == top_down:
                    unfound += 1
            if unfound == 0:
                break


        if moved or force_fixation: start = new_target
    return mt, scanpath

#reset_decision_ui(decision_ui, element_values2, color = True)
#reset_decision_ui(decision_ui)
#ui.visualise_UI(decision_ui)
#print(make_decision(decision_ui, element_values2))
#visualise_UI(decision_ui, path = make_decision(decision_ui, element_values2)[1])
