<template>
  <div class="modal fade" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header text-center">
          <div class="container">
            <div class="row">
              <div class="col-md-12">
                <h3>Hint</h3>
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
        <form method="POST" @submit.prevent="updateHint">
          <div class="modal-body">
            <div class="container">
              <div class="row">
                <div class="col-md-12">
                  <div class="form-group">
                    <label class="text-muted">
                      Hint<br />
                      <small>Markdown &amp; HTML are supported</small>
                    </label>
                    <!-- Explicitly don't put the markdown class on this because we will add it later -->
                    <textarea
                      type="text"
                      class="form-control"
                      name="content"
                      rows="7"
                      :value="this.content"
                      ref="content"
                    ></textarea>
                  </div>
                  <div class="form-group">
                    <label>
                      Type <br />
                      <small>What type of hint it is (what will you pay).</small>
                    </label><br>
                    <input type="radio" id="hint_standard" name="hint_type" value="0" v-model="radio">
                    <label for="0">Points</label><br>
                    <input type="radio" id="hint_standard" name="hint_type" value="1" v-model="radio">
                    <label for="1">Time</label><br>
                  </div>
                  <div class="form-group">
                    <label>
                      Cost<br />
                      <small>How many points it costs to see your hint.</small>
                    </label>
                    <input
                      type="number"
                      class="form-control"
                      name="cost"
                      v-model.lazy="cost"
                    />
                    <div class="form-group">
                    <label>
                      Time<br />
                      <small>How much time before the hint release. (mins)</small>
                    </label>
                    <input
                      type="number"
                      class="form-control"
                      name="cost"
                      v-model.lazy="time"
                    />
                    </div>
                  </div>
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
import CTFd from "core/CTFd";
import { bindMarkdownEditor } from "../../styles";

export default {
  name: "HintEditForm",
  props: {
    hint_id: Number
  },
  data: function() {
    return {
      cost: 0,
      time: 0,
      radio : "",
      content: null
    };
  },
  watch: {
    hint_id: {
      immediate: true,
      handler(val, oldVal) {
        if (val !== null) {
          this.loadHint();
        }
      }
    }
  },
  methods: {
    loadHint: function() {
      CTFd.fetch(`/api/v1/hints/${this.$props.hint_id}?preview=true`, {
        method: "GET",
        credentials: "same-origin",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json"
        }
      })
        .then(response => {
          return response.json();
        })
        .then(response => {
          if (response.success) {
            let hint = response.data;
            this.cost = hint.cost;
            this.content = hint.content;
            this.radio = hint.is_timed;
            this.time = hint.time;
            // Wait for Vue to update the DOM
            this.$nextTick(() => {
              // Wait a little longer because we need the modal to appear.
              // Kinda nasty but not really avoidable without polling the DOM via CodeMirror
              setTimeout(() => {
                let editor = this.$refs.content;
                bindMarkdownEditor(editor);
                editor.mde.codemirror.getDoc().setValue(editor.value);
                editor.mde.codemirror.refresh();
              }, 100);
            });
          }
        });
    },
    getCost: function() {
      return this.cost || 0;
    },
    getTime: function() {
      return this.time || 0;
    },
    getContent: function() {
      return this.$refs.content.value;
    },
    getRadio: function() {
      return this.radio 
    },
    updateHint: function() {
      let params = {}
      if(this.radio == "0"){
        params = {
        challenge_id: this.$props.challenge_id,
        content: this.getContent(),
        cost: this.getCost(),
        is_timed : 0,
        time : 0,
        }
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
      CTFd.fetch(`/api/v1/hints/${this.$props.hint_id}`, {
        method: "PATCH",
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
  },
  mounted() {
    if (this.hint_id) {
      this.loadHint();
    }
  },
  created() {
    if (this.hint_id) {
      this.loadHint();
    }
  }
};
</script>

<style scoped></style>
