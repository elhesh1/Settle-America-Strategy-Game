const hoverMap = {
    'FarmerJobGrid'  : ['FarmerJobToolTip','FarmersToolTipText','Job'],
    'HuntersJobGrid' : ['HuntersJobToolTip','HuntersToolTipText','Job'],
    'CooksJobGrid' : ['CooksJobToolTip','CooksToolTipText','Job'],
    'LoggersJobGrid' : ['LoggersJobToolTip','LoggersToolTipText','Job'],
    'ButchersJobGrid' : ['ButchersJobToolTip','ButchersToolTipText','Job'],
    'BuilderJobGrid' : ["BuildersJobToolTip",'BuildersToolTipText','Job'],
    'logcabinBuildGrid' : ['LogCabinToolTip', 'logCabinInner', 'Housing', 1, 'log cabin']

}

const hoverState = new Map();
const tooltipInProgress = new Map(); 

async function toggleHover() {
  const id = this.id;
  const tab = document.getElementById(hoverMap[id][0]);

  if (tooltipInProgress.get(id)) return;

  if (!hoverState.has(id) || hoverState.get(id) === 0) {
    tab.style.visibility = 'visible';
    hoverState.set(id, 1);
    
    tooltipInProgress.set(id, true);
    
    try {
      await tooltipSetupBuilding(hoverMap[id]);
    } catch (error) {
      console.error("Error setting up tooltip:", error);
    } finally {
      tooltipInProgress.set(id, false);
    }
  } 
  
}

async function toggleHoverOff() {
  const id = this.id;
  const tab = document.getElementById(hoverMap[id][0]);

  if (hoverState.has(id) && hoverState.get(id) === 1) {
    tab.style.visibility = 'hidden';
    hoverState.set(id, 0);
    if (!tooltipInProgress.get(id)) {
      tab.style.visibility = 'hidden';
    }
  } 
}





async function tooltipSetupBuilding(map) {
  
    let cost = document.getElementById(map[1]);
  //  console.log('ID    :  ', map[0], "   ", map, "  ", map[3])
    let resourceMap = await getResources();
    string = ''
    string +='<div class="flexitem ToolTipLine" width="80%" size="4"></div>'  //line
    string +='<div class="flexitem" id="Cost" style="text-align: center">' + map[2] + '</div>'    // type of item
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>'                                // line
    if (map[2] != 'Job') {
      let BuildingInfo = await getBuilding(map[3]);
      costList = BuildingInfo.buildingInfo.cost
      buildingInfo = BuildingInfo.buildingInfo
      costString = '';
      costString = '<div class="flexitem" id="Cost" style="text-align: center">' + 'Cost:' + '</div>';
      for (const key in costList) {
          costString +=`<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;">
          <div style="text-align: left; ">${resourceMap.resources[key-1].name}</div> <div style="text-align: right;">${costList[key]}</div></div>`;
      }
      string += costString;
      string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>'                                // line

      if (map[2] == 'Housing') {
        sum = Math.round(buildingInfo.value * buildingInfo.capacity)
       string +=  '<div class="flexitem" id="Cost" style="text-align: left; width: 100%">' + 'Each '+ map[4] + ' can house ' +  buildingInfo.capacity +  ' people.' 
       +  ' The ' +  buildingInfo.value + " " + map[4] + 's currently built house ' + sum + ' citizens' +  '</div>';

      }
    }

    cost.innerHTML = string;
}

async function getBuilding(user_id) {
  try {
      const response = await fetch(`http://127.0.0.1:5000/buildings/${user_id}`);
      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      return data;
  } catch (error) {
      console.error('There was a problem with your fetch operation:', error);
      throw error;
  }
}
