import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?" 
key = "3twovHJyHSWX4b397ckdi22ocrOK5d8t"

while True:
    orig = input("Ciudad de Origen: ")

    if orig.lower() == "salir" or orig.lower() == "q":
        break

    dest = input("Ciudad de Destino: ")

    if dest.lower() == "salir" or dest.lower() == "q":
        break

    url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("=============================================")
        print("Direcciones desde " + orig + " hasta " + dest)
        print("Duración del Viaje: " + json_data["route"]["formattedTime"])
        print("Kilómetros: {:.3f}".format(json_data["route"]["distance"]*1.61))
        print("Combustible Requerido (Ltr): {:.3f}".format((json_data["route"]["distance"]*1.61)/15))
        print("=============================================")

        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print(each["narrative"] + " ({:.3f} km)".format(each["distance"]*1.61))

        print("=============================================\n")

    elif json_status == 402:
        print("**********************************************")
        print("Código de Estado: " + str(json_status) + "; Entradas de usuario inválidas para una o ambas ubicaciones.")
        print("**********************************************\n")

    elif json_status == 611:
        print("**********************************************")
        print("Código de Estado: " + str(json_status) + "; Falta una entrada para una o ambas ubicaciones.")
        print("**********************************************\n")

    else:
        print("************************************************************************")
        print("Para el Código de Estado: " + str(json_status) + "; Consultar en:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")
