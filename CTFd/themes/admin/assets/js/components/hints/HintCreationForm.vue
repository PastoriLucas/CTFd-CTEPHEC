<template>
  <div class="modal fade" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header text-center">
          <div class="container">
            <div class="row">
              <div class="col-md-12">
                <h3>Hints</h3>
              </div>
            </div>
          </div>
          <button
            type="button"
            class="close"
            data-dismiss="modal"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <form method="POST" @submit.prevent="submitHint">
          <div class="modal-body">
            <div class="container">
              <div class="row">
                <div class="col-md-12">
                  <div class="form-group">
                    <label class="text-muted">
                      Hint<br />
                      <small>Markdown &amp; HTML are supported</small>
                    </label>
                    <textarea
                      type="text"
                      class="form-control markdown"
                      name="content"
                      rows="7"
                      ref="content"
                    ></textarea>
                  </div>

                  <div class="form-group">
                    <label>
                      Type <br />
                      <small>What type of hint it is (what will you pay).</small>
                    </label><br>
                    <input type="radio" id="hint_standard" name="hint_type" value="0" v-model="radio" required>
                    <label for="points">Points</label><br>
                    <input type="radio" id="hint_standard" name="hint_type" value="1" v-model="radio">
                    <label for="time">Time</label><br>
                  </div>

                  <div class="form-group">
                    <label>
                      Cost<br/>
                      <small>How many points it costs to see your hint.</small>
                    </label>
                    <input
                      type="number"
                      class="form-control"
                      name="cost"
                      v-model.lazy="cost"
                    />
                  </div>
                  <div class="form-group">
                  <label>
                    Time<br/>
                    <small>How much time before the hint release. (sec)</small>
                  </label>
                  <input
                    type="number"
                    class="form-control"
                    name="time"
                    v-model.lazy="time"
                  />
                  </div>
                  
                  <input type="hidden" id="hint-id-for-hint" name="id" />
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <div class="container">
              <div class="row">
                <div class="col-md-12">
                  <button class="btn btn-primary float-right">Submit</button>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HintCreationForm",
  props: {
    challenge_id: Number,
    hints: Array
  },
  data: function() {
    return {
      cost: 0,
      time: 0,
      radio : "",
    };
  },
  methods: {
    getCost: function() {
      return this.cost || 0;
    },
    getContent: function() {
      return this.$refs.content.value;
    },
    getTime: function() {
      return this.time;
    },
    submitHint: function() {
      let params = {}
      if(this.radio == "0"){
        params = {
        challenge_id: this.$props.challenge_id,
        content: this.getContent(),
        cost: this.getCost(),
        requirements: { prerequisites: this.selectedHints }
        };
      }
      if(this.radio == "1"){
        params = {
        challenge_id: this.$props.challenge_id,
        content: this.getContent(),
        is_timed: 1,
        time : this.getTime(),
        cost : 0,
        }
      }
    
      CTFd.fetch("/api/v1/hints", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify(params)
      })
        .then(response => {
          return response.json();
        })
        .then(response => {
          if (response.success) {
            this.$emit("refreshHints", this.$options.name);
          }
        });
    }
  }
};
</script>

<style scoped></style>
