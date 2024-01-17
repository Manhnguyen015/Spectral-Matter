import os
import guilib as ui
import numpy as np


widgets = {"textbox": None, "point": []}


def read_data(folder_path):
    # read data from folder
    all_intensity = []
    faulty_list = []
    filelist = os.listdir(folder_path)
    for eachfile in filelist:
        energy_tempo = []
        intensity_tempo = []
        path = os.path.join(folder_path, eachfile)
        try:
            with open(path) as source:
                for row in source.readlines():
                    if row == "\n":
                        pass
                    else:
                        try:
                            energy, intensity = row.split(" ")
                            energy_tempo.append(float(energy))
                            intensity_tempo.append(float(intensity))
                        except ValueError:
                            faulty_list.append(eachfile)
        except (IOError, UnicodeDecodeError):
            faulty_list.append(eachfile)
        else:
            if len(intensity_tempo) == 500:
                if len(energy_tempo) == 500:
                    all_intensity.append(intensity_tempo)
                    widgets["energy"] = energy_tempo
                else:
                    pass
            else:
                pass
    widgets["intensity"] = sum_list(all_intensity)
    return faulty_list


def sum_list(biglist):
    # sum list funcition
    sumlist = []
    for eachlist in biglist:
        if eachlist == biglist[0]:
            for i, y in enumerate(eachlist):
                sumlist.append(y)
        else:
            for i, y in enumerate(eachlist):
                sumlist[i] = sumlist[i] + y
    return sumlist


def open_folder():
    # open folder
    widgets["folderpath"] = ui.open_folder_dialog(
        "Choose folder", r"/Users/trung/Downloads/spektridata"
    )
    faultylist = read_data(widgets["folderpath"])
    if faultylist == []:
        pass
    elif len(faultylist) >= 1:
        message2 = "Cannot read {} files.".format(len(faultylist))
        ui.open_msg_window("Error message", message2, error=True)


def choose_point(event):
    # choose point when click
    x = event.xdata
    y = event.ydata
    xlist = widgets["energy"]
    ylist = widgets["intensity"]
    for i, each_x in enumerate(xlist):
        if each_x <= x <= xlist[i + 1]:
            if ylist[i] <= y <= ylist[i + 1]:
                widgets["point"].append((x, y))
                message1 = "You have chosen x = {}, y = {}".format(x, y)
                ui.write_to_textbox(widgets["textbox"], message1)
            elif ylist[i] >= y >= ylist[i + 1]:
                widgets["point"].append((x, y))
                message2 = "You have chosen x = {}, y = {}".format(x, y)
                ui.write_to_textbox(widgets["textbox"], message2)
            else:
                pass
        else:
            pass


def calculate_parameters(x_1, y_1, x_2, y_2):
    # calculate parameters
    try:
        m = float((y_2 - y_1) / (x_2 - x_1))
        c = float((x_2 * y_1 - x_1 * y_2) / (x_2 - x_1))
    except ZeroDivisionError:
        message = "The line is vertical, it doesn't have an equation."
        ui.write_to_textbox(widgets["textbox"], message)
    else:
        return m, c


def draw_figure(frame):
    # draw figure
    canvas, widgets["figure"], subplot = ui.create_figure(
        frame, choose_point, width=900, height=500
    )
    subplot.set_xlabel("Binding energy (eV)")
    subplot.set_ylabel("Intensity (arbitrary units)")
    subplot.plot(widgets["energy"], widgets["intensity"])


def make_belong(x, y):
    # check x,y
    for i, energy in enumerate(widgets["energy"]):
        if energy <= x <= widgets["energy"][i + 1]:
            if widgets["intensity"][i] <= y <= widgets["intensity"][i + 1]:
                return i
            elif widgets["intensity"][i] >= y >= widgets["intensity"][i + 1]:
                return i
            else:
                pass
        else:
            pass


def only_peak():
    # peak
    new_y = []
    x_1, y_1 = widgets["point"][0]
    x_2, y_2 = widgets["point"][1]
    if x_1 == x_2 and y_1 == y_2:
        ui.open_msg_window(
            "Error message", "These points should not be the same.", error=True
        )
    else:
        slope, y_intercept = calculate_parameters(x_1, y_1, x_2, y_2)
        for i, x in enumerate(widgets["energy"]):
            y_new = widgets["intensity"][i] - (slope * x + y_intercept)
            new_y.append(y_new)
    return new_y


def calculate_peak():
    # calculate peak
    xlist = []
    ylist = []
    if len(widgets["point"]) < 2:
        ui.open_msg_window(
            "Error message", "Please choose 2 different points", error=True
        )
    else:
        x_1, y_1 = widgets["point"][-2]
        x_2, y_2 = widgets["point"][-1]
        index1 = make_belong(x_1, y_1)
        index2 = make_belong(x_2, y_2)
        if x_1 == x_2:
            ui.open_msg_window(
                "Error message", "Please choose 2 different points", error=True
            )
        else:
            if x_1 < x_2:
                xlist = widgets["energy"][index1:index2]
                ylist = widgets["intensity"][index1:index2]
            else:
                xlist = widgets["energy"][index2:index1]
                ylist = widgets["intensity"][index2:index1]
            area = np.trapz(ylist, xlist)
            message = "The intensity of peak is {}.".format(area)
            ui.write_to_textbox(widgets["textbox"], message)


def save():
    # save programme
    path = ui.open_save_dialog("Save your figure in", r"/Users/trung/Desktop/spectral")
    widgets["figure"].savefig(path)


def load():
    if len(widgets["point"]) < 2:
        ui.open_msg_window(
            "Error message", "Please choose 2 different points", error=True
        )
    else:
        ui.remove_component(widgets["figureframe"])
        widgets["figureframe"] = ui.create_frame(widgets["window"], ui.TOP)
        widgets["intensity"] = only_peak()
        draw_figure(widgets["figureframe"])


def reset():
    # reset programme
    ui.remove_component(widgets["figureframe"])
    widgets["figureframe"] = ui.create_frame(widgets["window"], ui.TOP)
    read_data(widgets["folderpath"])
    widgets["point"] = []
    draw_figure(widgets["figureframe"])


def main():
    widgets["window"] = ui.create_window("Spectral")
    widgets["figureframe"] = ui.create_frame(widgets["window"], ui.TOP)
    textframe = ui.create_frame(widgets["window"], ui.BOTTOM)
    buttonframe = ui.create_frame(textframe, ui.LEFT)
    ui.create_button(buttonframe, "quit", ui.quit)
    widgets["textbox"] = ui.create_textbox(textframe, width=80, height=20)
    open_folder()
    draw_figure(widgets["figureframe"])
    widgets["loadbutton"] = ui.create_button(buttonframe, "load", load)
    ui.create_button(buttonframe, "peak", calculate_peak)
    ui.create_button(buttonframe, "save", save)
    ui.create_button(buttonframe, "reset", reset)
    ui.start()


if __name__ == "__main__":
    main()
