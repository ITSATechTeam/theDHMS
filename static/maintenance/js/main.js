// TABLE STARTS HERE
const topCheckBox = document.querySelector('.topCheckBox input')
const sectionCheckBox = document.querySelectorAll('.sectionCheckBox input')
const sectionCheckBoxEach = document.querySelectorAll('.sectionCheckBoxinput')
const maintenanceReqeustCount = parseInt(document.querySelector('.maintenanceReqeustCount').innerHTML)


let detailsTabCountInnner = document.querySelector('.detailsTabCountInnner strong')
let detailsTabOut = document.querySelector('.detailsTabOut')
let detailsTabInnerEdit = document.querySelector('.detailsTabInnerEdit')
let detailsTabInnerViewDetails = document.querySelector('.detailsTabInnerViewDetails')
let selectedRequest = document.querySelector('.sectionCheckBox p')
let maintainName = document.querySelectorAll('.maintainName p')
let maintainNameID = document.getElementById('maintainName')
let maintainNameIDMain = document.querySelectorAll('.maintainName p')
let maintainNameIDMain2= document.querySelectorAll('.maintainName i')
let ExportDataHere = document.querySelector('.ExportDataHere input')
let requesttoviewdetails = document.querySelector('.requesttoviewdetails input')

// ID SENDING SECTION STARTS HERE
let devicesID = document.querySelectorAll('.maintainName strong')
let sectionCheckID = document.querySelector('.sectionCheckID')
// console.log(devicesID)
let idforedit = document.querySelector('.idforedit input')
let deviceToDelete = document.querySelector('.deviceToDelete input')
// console.log(idforedit)

// DELETED AND EXPORT BUTTON FOR GENERAL AND NOT GENERAL SELECTIONS
let notSelectionDelete = document.querySelector('.notSelectionDelete')
let notSelectionExport = document.querySelector('.notSelectionExport')
// GENERALS BELOW
let generalSelectionDelete = document.querySelector('.generalSelectionDelete')
let generalSelectionExport = document.querySelector('.generalSelectionExport')

topCheckBox.addEventListener('change', () => {
    if (topCheckBox.checked === true){
        console.log('topCheckBox is checked true now')
        notSelectionDelete.style.display = 'none'
        notSelectionExport.style.display = 'none'
        // 
        generalSelectionDelete.style.display = 'block';
        generalSelectionExport.style.display = 'block';
    }else{
        console.log('topCheckBox is NOT checked true now')
        notSelectionDelete.style.display = 'block'
        notSelectionExport.style.display = 'block'
        // 
        generalSelectionDelete.style.display = 'none';
        generalSelectionExport.style.display = 'none';
    }
})





// CHECK BOX COUNTS SECTION STARTS HERE
let trueBoxes = 0;
let DataArray = []
let DataArrayFirst;
let IDArray = []
function checkBoxFunctions(each){
    each.addEventListener('change', () => {
        maintainNameIDMain.forEach((e) => {
            let eValue = e.innerHTML
            if(eValue.includes(each.value)){
                DataArray.push(eValue);
                console.log(DataArray)
                return DataArray, 
                ExportDataHere.value = DataArray, 
                idforedit.value = DataArray, 
                deviceToDelete.value = DataArray,
                requesttoviewdetails.value = DataArray
            }
        })
        if (each.checked === true){
            trueBoxes += 1;
        }else{
            trueBoxes -= 1
        }
        detailsTabCountInnner.innerHTML = ` ${trueBoxes} `
        if (trueBoxes <= 0){
            trueBoxes = 0;
            detailsTabOut.style.display = 'none'
        }else{
            detailsTabOut.style.display = 'block'
        }
        if (trueBoxes > 1){
            detailsTabInnerEdit.style.display = 'none'
            detailsTabInnerViewDetails.style.display = 'none'
        }else if(trueBoxes <= 1){
            detailsTabInnerEdit.style.display = 'block'
            detailsTabInnerViewDetails.style.display = 'block'
        }
        
        if(trueBoxes < maintenanceReqeustCount){
            topCheckBox.checked = false;
        } else if (trueBoxes = maintenanceReqeustCount){
            topCheckBox.checked = true;
            console.log("all boxes are checked 'true' now");
            notSelectionDelete.style.display = 'none'
            notSelectionExport.style.display = 'none'
            // 
            generalSelectionDelete.style.display = 'block';
            generalSelectionExport.style.display = 'block';
        }
    })
}

// EACH CHECKBOX SELECTION SETTINGS STARTS HERE
sectionCheckBox.forEach(each => {
    checkBoxFunctions(each)
})
// EACH CHECKBOX SELECTION SETTINGS ENDS HERE



// GENERAL SECTION EFFECT STARTS HERE
topCheckBox.addEventListener('change', () => {
    if (topCheckBox.checked === true){
            sectionCheckBox.forEach(e => {
                e.checked = true
                detailsTabCountInnner.innerHTML = `${maintenanceReqeustCount} `
                trueBoxes = maintenanceReqeustCount

                if (trueBoxes <= 0){
                    trueBoxes = 0;
                    detailsTabOut.style.display = 'none'
                }else{
                    detailsTabOut.style.display = 'block'
                }
                if (trueBoxes > 1){
                    detailsTabInnerEdit.style.display = 'none'
                    detailsTabInnerViewDetails.style.display = 'none'
                }else if(trueBoxes <= 1){
                    detailsTabInnerEdit.style.display = 'block'
                    detailsTabInnerViewDetails.style.display = 'block'
                }

            })
        
    }else{
        sectionCheckBox.forEach(e => {
            e.checked = false
            
            detailsTabCountInnner.innerHTML = `0 `
            trueBoxes = 0
            if (trueBoxes <= 0){
                trueBoxes = 0;
                detailsTabOut.style.display = 'none'
            }else{
                detailsTabOut.style.display = 'block'
            }
            if (trueBoxes > 1){
                detailsTabInnerEdit.style.display = 'none'
                detailsTabInnerViewDetails.style.display = 'none'
            }else if(trueBoxes <= 1){
                detailsTabInnerEdit.style.display = 'block'
                detailsTabInnerViewDetails.style.display = 'block'
            }
        })
    }
})
// GENERAL SECTION EFFECT ENDS HERE
// CHECKBOX SECTION STARTS HERE


// TABLE ENDS HERE

// EDIT AND DELETE BUTTON SELECTION FUNCTIONALITY STARTS HERE

let sectionToReplace = document.querySelector('.sectionToReplace')





// EDIT AND DELETE BUTTON SELECTION FUNCTIONALITY ENDS HERE


// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashMaintain = document.querySelector('.alert strong')
if(flashMaintain){
    console.log('flashMaintain around')
    setTimeout(() => {
        flashMaintain.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE