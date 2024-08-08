const hoverMap = {
    'FarmerJobGrid'  : ['FarmerJobToolTip','FarmersToolTipText','Job','farmer',1],
    'HuntersJobGrid' : ['HuntersJobToolTip','HuntersToolTipText','Job','hunter',2],
    'CooksJobGrid' : ['CooksJobToolTip','CooksToolTipText','Job','cook',3],
    'LoggersJobGrid' : ['LoggersJobToolTip','LoggersToolTipText','Job','logger',4],
    'ButchersJobGrid' : ['ButchersJobToolTip','ButchersToolTipText','Job','butcher',11],
    'BuilderJobGrid' : ["BuildersJobToolTip",'BuildersToolTipText','Job','builder',15],
    'logcabinBuildGrid' : ['LogCabinToolTip', 'logCabinInner', 'Housing', 1, 'log cabin'],
    'topFoodBar' : ['HealthToolTip','HealthToolTipText' , 'Value'],
    'RationGrid' : ['RationToolTip', 'RationToolTipText', 'Value']
}

const hoverState = new Map();
const tooltipInProgress = new Map(); 

async function toggleHover() {
  console.log(" hovering  ,"   , this.id);
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
    let resourceMap = await getResources();
    string = ''
    string +='<div class="flexitem ToolTipLine" width="80%" size="4"></div>'  //line
    string +='<div class="flexitem" id="Cost" style="text-align: center">' + map[2] + '</div>'    // type of item
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>'                                // line

    if (map[2] == 'Housing') {
      let BuildingInfo = await getBuilding(map[3]);
      costList = BuildingInfo.buildingInfo.cost
      buildingInfo = BuildingInfo.buildingInfo
      costString = '';
      costString = '<div class="flexitem" id="Cost" style="text-align: center">' + 'Cost:' + '</div>';
      for (const key in costList) {
          costString +=`<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;">
          <div style="text-align: left; ">${resourceMap.resources[key-1].name}</div> <div style="text-align: right;">${costList[key]}</div></div>`;
      }


      costString +=`<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;">
      <div style="text-align: left; ">Work</div> <div style="text-align: right;">${buildingInfo.work}</div></div>`;


      string += costString;
      string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>'                                // line

      if (map[2] == 'Housing') {
        sum = Math.round(buildingInfo.value * buildingInfo.capacity)
       string +=  '<div class="flexitem" id="Cost" style="text-align: left; width: 100%">' + 'Each '+ map[4] + ' can house ' +  buildingInfo.capacity +  ' people.' 
       +  ' The ' +  buildingInfo.value + " " + map[4] + 's currently built house ' + sum + ' citizens' +  '</div>';

      }
    }
    else if (map[0] == 'HealthToolTip') {
      string += await HealthToolTipParagraphTextToBeAddedToTheString();
    } 
    else if (map[0] == 'RationToolTip') {
      string += await RationingString();
    }
    else if (map[2] == 'Job') {
      string += '<div class="flexitem" id="Cost" style="text-align: center">' + ' Change:' + map[3] +  '</div>';
      let season = await getValue('contacts/',8)
      let r = await getContact(map[4]);
      string += '<div class="flexitem" id="Cost" style="text-align: center">' + ' Change: ' + r['efficiency']['season'][season] +  '</div>';

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

async function RationingString() {
 string = '';
 string += '<div class="flexitem" style="text-align: left; width: 100%">'



 string += "You can ration food to make it last longer"
 string += '</div>';
 string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' // line
 string += '<div class="flexitem" style="text-align: left; width: 100%">'
 string += "Health = (0.15 + 0.85*Rationing)*Other Stuff"
 string += '</div>';
 return string;
}


async function HealthToolTipParagraphTextToBeAddedToTheString() {
  // need health value, current numbers of 
  let nFoodTypes = await getValue('contacts/',17);
  let health = await getValue('contacts/',13);
  let rationP = await getValue('contacts/',12);
  let pop = await getValue('contacts/',5);
  let h = await getBuilding(1) 
  let housed = h['buildingInfo'].value * h['buildingInfo'].capacity

  string = ""

  string += '<div class="flexitem" style="text-align: left; width: 100%">'
  string += 'The health of your colony is very important as it effects citizens ability to do jobs. If your health falls below 50, citizens will start to die off'
  string += '</div>';
  string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' // line
  string += '<div class="flexitem" style="text-align: left; width: 100%">' ;
  string += 'Your current health of ' + health + ' is affected by your rationing % of ' + rationP + ' and number of food groups : ' + nFoodTypes + '. Providing all 4 food groups is good for health, but only 1 is needed.';
  string += '</div>';
  string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' // line

  string += '<div class="flexitem" style="text-align: left; width: 100%">'
  string += 'Lack of housing effects health. While it has a small effect in summer, it can be detrimental in the winter'
  string += '</div>';

  string +=`<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;">
          <div style="text-align: left; ">Housing Provided: </div> <div style="text-align: right;">${ housed + ' / ' + pop}</div></div>`;
 


  return string;
}