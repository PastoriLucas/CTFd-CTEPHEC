import "./main";
import CTFd from "core/CTFd";
import $ from "jquery";
import { ezAlert, ezQuery } from "core/ezq";

function deleteSelectedExplanations(_event) {
  let explanationIDs = $("input[data-explanation-id]:checked").map(function() {
    return $(this).data("explanation-id");
  });
  let target = explanationIDs.length === 1 ? "explanation" : "explanations";

  ezQuery({
    title: "Delete Explanations",
    body: `Are you sure you want to delete ${explanationIDs.length} ${target}?`,
    success: function() {
      const reqs = [];
      for (var expID of explanationIDs) {
        reqs.push(
          CTFd.fetch(`/api/v1/explanations/${expID}`, {
            method: "DELETE"
          })
        );
      }
      Promise.all(reqs).then(_responses => {
        window.location.reload();
      });
    }
  });
}


$(() => {
  $("#explanation-delete-button").click(deleteSelectedExplanations);
});
