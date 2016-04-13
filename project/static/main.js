// custom javascript

var testCases = 1;

function addChallenge() {
  var newChallenge = {};

  var id = assignId("challenge");
  var name = $("#challengeName").val();
  var description = $("#challengeDesc").val();
  var deadline = $('#datetimepicker1').data("DateTimePicker").date();
  console.log("raw deadline = " + deadline);

  newChallenge.id = id;
  console.log("newChallenge.id = " + newChallenge.id);

  newChallenge.name = name;
  console.log("newChallenge.name = " + newChallenge.name);

  newChallenge.description = description;
  console.log("newChallenge.description = " + newChallenge.description);

  newChallenge.deadline = deadline["_d"];
  console.log("newChallenge.deadline = " + newChallenge.deadline);

  challenges.push(newChallenge);
  console.log(challenges);
}

function init() {
  $("#closeFloater").on("click", function(){
    $("#floatingPlanner").css("display", "none");
  })

  $("#cancelExForm").on('click', function() {
    alert("cancel button clicked");
  });

  $("#createChallenge").on('click', function() {
    addChallenge();
  });

  $("#addTestCaseBtn").on("click", function() {
    testCases += 1;
    var testCaseName = "TestCase" + testCases;
    var hintName = "hint" + testCases;
    $("#hintFieldset").append(
      $("<label class='sm-label' for="+testCaseName+"></label>").html("Test Case " + testCases),
      $("<input type='text' class='form-control' id="+testCaseName+" name="+testCaseName+" placeholder='enter assertion here'/>"),
      $("<label class='sm-label hint-label' for='hint'></label>").html("Hint " + testCases),
      $("<input type='text' class='form-control hint-input' id="+hintName+" name="+hintName+"/>")
    )
  })
}

window.onload = init;
