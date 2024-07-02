
'''
    I may want to remove this portion as the new graph will be plugged
    into the patch.cab app.
'''


def graphviz():
    global quiet, direction
    linetypes = {
        "audio": {"style": "bold"},
        "cv": {"color": "gray"},
        "gate": {"color": "red", "style": "dashed"},
        "trigger": {"color": "orange", "style": "dashed"},
        "pitch": {"color": "blue"},
        "clock": {"color": "purple", "style": "dashed"}
    }
    if direction == "DN":
        rank_dir_token = "rankdir = BT;\n"
        from_token = ":s  -> "
        to_token = ":n  "
    else:
        rank_dir_token = "rankdir = LR;\n"
        from_token = ":e  -> "
        to_token = ":w  "
    if not quiet:
        print("Generating signal flow code for GraphViz.")
        print("Copy the code between the line break and paste it into https://dreampuf.github.io/GraphvizOnline/ to download a SVG / PNG chart.")
    conn = []
    total_string = ""
    if not quiet: print("-------------------------")
    print("digraph G{\n" + rank_dir_token + "splines = polyline;\nordering=out;")
    total_string += "digraph G{\n" + rank_dir_token + "splines = polyline;\nordering=out;\n"
    for module in sorted(mainDict["modules"]):
        # Get all outgoing connections:
        outputs = mainDict["modules"][module]["connections"]["out"]
        module_outputs = ""
        out_count = 0
        for out in sorted(outputs):
            out_count += 1
            out_formatted = "_" + re.sub('[^A-Za-z0-9]+', '', out)
            module_outputs += "<" + out_formatted + "> " + out.upper()
            if out_count < len(outputs.keys()):
                module_outputs += " | "
            connections = outputs[out]
            for c in connections:
                line_style_array = []
                graphviz_parameters = [
                    "color", "weight", "style", "arrowtail", "dir"]
                for param in graphviz_parameters:
                    if param in c:
                        line_style_array.append(param + "=" + c[param])
                    elif param in linetypes[c["connection_type"]]:
                        line_style_array.append(
                            param + "=" + linetypes[c["connection_type"]][param])
                if len(line_style_array) > 0:
                    line_style = "[" + ', '.join(line_style_array) + "]"
                else:
                    line_style = ""
                in_formatted = "_" + \
                    re.sub('[^A-Za-z0-9]+', '', c["input_port"])
                connection_line = module.replace(" ", "") + ":" + out_formatted + from_token + \
                    c["input_module"].replace(
                        " ", "") + ":" + in_formatted + to_token + line_style
                conn.append([c["input_port"], connection_line])

        # Get all incoming connections:
        inputs = mainDict["modules"][module]["connections"]["in"]
        module_inputs = ""
        in_count = 0
        for inp in sorted(inputs):
            inp_formatted = "_" + re.sub('[^A-Za-z0-9]+', '', inp)
            in_count += 1
            module_inputs += "<" + inp_formatted + "> " + inp.upper()
            if in_count < len(inputs.keys()):
                module_inputs += " | "

        # Get all parameters:
        params = mainDict["modules"][module]["parameters"]
        module_params = ""
        param_count = 0
        for par in sorted(params):
            param_count += 1
            module_params += par.title() + " = " + params[par]
            if param_count < len(params.keys()):
                module_params += r'\n'

        # If module contains parameters
        if module_params != "":
            # Add them below module name
            middle = "{{" + module.upper() + "}|{" + module_params + "}}"
        else:
            # Otherwise just display module name
            middle = module.upper()

        final_box = module.replace(
            " ", "") + "[label=\"{ {" + module_inputs + "}|" + middle + "| {" + module_outputs + "}}\"  shape=Mrecord]"
        print(final_box)
        total_string += final_box + "; "

    # Print Connections
    for c in sorted(conn):
        print(c[1])
        total_string += c[1] + "; "

    if len(mainDict["comments"]) != 0:
        format_comments = ""
        comments_count = 0
        for comment in mainDict["comments"]:
            comments_count += 1
            format_comments += "{" + comment + "}"
            if comments_count < len(mainDict["comments"]):
                format_comments += "|"
        format_comments = "comments[label=<{{{<b>PATCH COMMENTS</b>}|" + format_comments + "}}>  shape=Mrecord]"
        print(format_comments)

    print("}")
    total_string += "}"

    if not quiet:
        print("-------------------------")
        print()
    return total_string
