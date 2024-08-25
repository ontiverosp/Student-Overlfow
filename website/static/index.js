function deleteQuestion(questionId) {
    fetch("./delete-question", {
      method: "POST",
      body: JSON.stringify({ questionId: questionId }),
    }).then((_res) => {
      window.location.href = "/my-questions";
    });
  }

function toQuestion(questionId){window.location.href = "/question/"+questionId}

function editQuestion(questionId){window.location.href = "/edit/"+questionId}