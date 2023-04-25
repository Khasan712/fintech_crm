const addBtn = document.getElementById("addBtn");
const card = document.getElementById("card");
const editHomeWork = document.getElementById("editHomeWork");
const editCard = document.getElementById("editCard");

const deleteHomeWorkMedia = document.getElementById("deleteHomeWorkMedia");
const deleteHomeWorkCard = document.getElementById("deleteHomeWorkCard");




const updatedGuideOrTaskTextBTN = document.getElementById("editGuideOrTaskTextID");
const editGuideOrTaskTextCard = document.getElementById("editGuideOrTaskText");


const deleteGuideOrTaskTextBTN = document.getElementById("deleteGuideOrTaskTextID");
const deleteGuideOrTaskTextCard = document.getElementById("deleteGuideOrTaskText");


const editGuideOrTaskFileBTN = document.getElementById("editGuideOrTaskFileID");
const editGuideOrTaskFileCard = document.getElementById("editGuideOrTaskFileCard");

const deleteGuideOrTaskFileBTN = document.getElementById("deleteGuideOrTaskFileID");
const deleteGuideOrTaskFileCard = document.getElementById("deleteGuideOrTaskFile");


const addBookPresentationBTN = document.getElementById("add-book-presentation");
const addBookPresentationCard = document.getElementById("addBookPresentationCard");

const addProjectBTN = document.getElementById("add-project");
const addProjectCard = document.getElementById("addProjectCard");

const editProjectBTN = document.getElementById("edit-project");
const editProjectCard = document.getElementById("editProjectCard");

const deleteProjectBTN = document.getElementById("delete-project");
const deleteProjectCard = document.getElementById("deleteProjectCard");

const addExam = document.getElementById("addExam");
const addExamCard = document.getElementById("addExamCard");

const deleteExam = document.getElementById("deleteExam");
const deleteExamCard = document.getElementById("deleteExamCard");

const addExamItemBTN = document.getElementById("addExamItemID");
const addExamItemCard = document.getElementById("addExamItemCard");

const editExamItemBTN = document.getElementById("editExamItemID");
const editExamItemCard = document.getElementById("editExamItemCard");

const deleteExamItemBTN = document.getElementById("deleteExamItemID");
const deleteExamItemCard = document.getElementById("deleteExamItemCard");

const addExamItemStudentBTN = document.getElementById("addExamItemStudentID");
const addExamItemStudentCard = document.getElementById("addExamItemStudentCard");

const editExamItemStudentBTN = document.getElementById("editExamItemStudentID");
const editExamItemStudentCard = document.getElementById("editExamItemStudentCard");

const deleteExamItemStudentBTN = document.getElementById("deleteExamItemStudentID");
const deleteExamItemStudentCard = document.getElementById("deleteExamItemStudentCard");


const addGroupBTN = document.getElementById("addGroupID");
const addGroupCard = document.getElementById("addGroupCard");


const selectStudentBTN = document.getElementById("selectStudentID");
const selectStudentCard = document.getElementById("selectStudentCard");

const editDeleteStudentFromGroupBTN = document.getElementById("editDeleteStudentFromGroupID");
const editDeleteStudentFromGroupCard = document.getElementById("editDeleteStudentFromGroupCard");


function openBtn() {
  card.classList.add("active");
}
function closeLesson() {
  card.classList.remove("active");
}



function editFile() {
  editCard.classList.add("active");
}
function closeEdit() {
  editCard.classList.remove("active");
}




function deleteFile() {
  deleteHomeWorkCard.classList.add("active");
}
function closeDelete() {
  deleteHomeWorkCard.classList.remove("active");
}





function editGuideOrTaskTextOpen() {
  editGuideOrTaskTextCard.classList.add("active");
}
function closeEditGuideOrTaskText() {
  editGuideOrTaskTextCard.classList.remove("active");
}


function deleteGuideOrTaskTextOpen() {
  deleteGuideOrTaskTextCard.classList.add("active");
}
function closeDeleteGuideOrTaskText() {
  deleteGuideOrTaskTextCard.classList.remove("active");
}



function editGuideOrTaskFileOpen() {
  editGuideOrTaskFileCard.classList.add("active");
}
function closeEditGuideOrTaskFile() {
  editGuideOrTaskFileCard.classList.remove("active");
}



function deleteGuideOrTaskFileOpen() {
  deleteGuideOrTaskFileCard.classList.add("active");
}
function closeDeleteGuideOrTaskFile() {
  deleteGuideOrTaskFileCard.classList.remove("active");
}


function addBookPresentation() {
  addBookPresentationCard.classList.add("active");
}
function closeaddBookPresentation() {
  addBookPresentationCard.classList.remove("active");
}


function addProject() {
  addProjectCard.classList.add("active");
}
function closeProjectBtn() {
  addProjectCard.classList.remove("active");
}


function editProjectBtn() {
  editProjectCard.classList.add("active");
}
function closeEditProjectBtn() {
  editProjectCard.classList.remove("active");
}


function deleteProjectBtn() {
  deleteProjectCard.classList.add("active");
}
function closeDeleteProjectBtn() {
  deleteProjectCard.classList.remove("active");
}


function addExamBtn() {
  addExamCard.classList.add("active");
}
function closeAddExamBtn() {
  addExamCard.classList.remove("active");
}


function deleteExamBtn() {
  deleteExamCard.classList.add("active");
}
function closeDeleteExamBtn() {
  deleteExamCard.classList.remove("active");
}

function addExamItemOpen() {
  addExamItemCard.classList.add("active");
}
function addExamItemClose() {
  addExamItemCard.classList.remove("active");
}


function editExamItemOpen() {
  editExamItemCard.classList.add("active");
}
function closeEditExamItem() {
  editExamItemCard.classList.remove("active");
}

function deleteExamItemOpen() {
  deleteExamItemCard.classList.add("active");
}
function deleteExamItemClose() {
  deleteExamItemCard.classList.remove("active");
}


function addExamItemStudentOpen() {
  addExamItemStudentCard.classList.add("active");
}
function addExamItemStudentClose() {
  addExamItemStudentCard.classList.remove("active");
}

function editExamItemStudentOpen() {
  editExamItemStudentCard.classList.add("active");
}
function editExamItemStudentClose() {
  editExamItemStudentCard.classList.remove("active");
}

function deleteExamItemStudentOpen() {
  deleteExamItemStudentCard.classList.add("active");
}
function deleteExamItemStudentClose() {
  deleteExamItemStudentCard.classList.remove("active");
}


function addGroupOpen() {
  addGroupCard.classList.add("active");
}
function addGroupClose() {
  addGroupCard.classList.remove("active");
}


function selectStudentOpen() {
  selectStudentCard.classList.add("active");
}
function selectStudentClose() {
  selectStudentCard.classList.remove("active");
}


function editDeleteStudentFromGroupOpen() {
  editDeleteStudentFromGroupCard.classList.add("active");
}
function editDeleteStudentFromGroupClose() {
  editDeleteStudentFromGroupCard.classList.remove("active");
}