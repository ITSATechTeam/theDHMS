from dhmsadminboard.models import technicianModel


def FindTechniciansInLocation(location):
    AllFoundTechnicians = []    
    foundTechnicianData = technicianModel.objects.filter(technicianLocation = location)
    for foundTechnicianData in foundTechnicianData:
        technicianName = foundTechnicianData.technicianName
        technicianEmail = foundTechnicianData.technicianEmail
        technicianPhone = foundTechnicianData.technicianPhoneNumber
        technicianLocation = foundTechnicianData.technicianLocation
        
        AllfoundTechnicianData = {
            'technicianName' : technicianName,
            'technicianEmail' : technicianEmail,
            'technicianPhone' : technicianPhone,
            'technicianLocation' : technicianLocation,
        }
        AllFoundTechnicians.append(AllfoundTechnicianData)
    return AllFoundTechnicians
        