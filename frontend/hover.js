const hoverMap = {
    'FarmerJobGrid'  : ['FarmerJobToolTip','TEST'],
    'HuntersJobGrid' : ['HuntersJobToolTip','TEST'],
    'CooksJobGrid' : ['CooksJobToolTip','TEST'],
    'LoggersJobGrid' : ['LoggersJobToolTip','TEST'],
    'ButchersJobGrid' : ['ButchersJobToolTip','TEST'],
    'BuilderJobGrid' : ["BuildersJobToolTip",'TEST'],
    'logcabinBuildGrid' : ['LogCabinToolTip', 'TEST']

}

async function toggleHover() {
    id = this.id
    const tab = document.getElementById(hoverMap[id][0]); //.style.visibility = "visible";


    switch (id) {
        case 'FarmerJobGrid':
          break;
        case 'HuntersJobGrid':
          break;
        case 'CooksJobGrid':
          break;         
        case 'LoggersJobGrid':
            break;
        case 'ButchersJobGrid':
            break;
        case 'BuilderJobGrid':
            break;
        case 'logcabinBuildGrid':
            await tooltipSetupBuilding(id)
            break;
      }
    tab.style.visibility = 'visible';
 }

 function toggleHoverOff() {
    const tab = document.getElementById(hoverMap[this.id][0]); //.style.visibility = "visible";
    tab.style.visibility = 'hidden';
 }

async function tooltipSetupBuilding(id) {
    console.log('ID    :  ', id)
    let cost = document.getElementById('logCabinInner');
    cost.innerHTML = '<div class="flexitem" id="Cost" style="text-align: center">' + 'Cost:' + 
    '</div><div class="flexitem" style="text-align: left">' + 22222 + 
    '</div><div class="flexitem">' + 33333 +  '</div>';
}

