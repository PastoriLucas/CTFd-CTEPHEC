<template>
  <div>
    <table id="filesboard" class="table table-striped">
      <thead>
        <tr>
          <td class="text-center"><b>File</b></td>
        </tr>
      </thead>
      <tbody>
        <tr v-for="file in files" :key="file.id">
          <td class="text-center">
            <a :href="`${urlRoot}/files/${file.location}`">{{
              file.location.split("/").pop()
            }}</a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ezQuery } from "core/ezq";
import { default as helpers } from "core/helpers";
import CTFd from "core/CTFd";

export default {
  props: {
    challenge_id: Number
  },
  data: function() {
    return {
      files: [],
      urlRoot: CTFd.config.urlRoot
    };
  },
  methods: {
    loadFiles: function() {
      CTFd.fetch(`/api/v1/challenges/${this.$props.challenge_id}/files`, {
        method: "GET"
      })
        .then(response => {
          return response.json();
        })
        .then(response => {
          if (response.success) {
            this.files = response.data;
          }
        });
    },
    addFiles: function() {
      let data = {
        challenge: this.$props.challenge_id,
        type: "challenge"
      };
      let form = this.$refs.FileUploadForm;
      helpers.files.upload(form, data, _response => {
        setTimeout(() => {
          this.loadFiles();
        }, 700);
      });
    },
    deleteFile: function(fileId) {
      ezQuery({
        title: "Delete Files",
        body: "Are you sure you want to delete this file?",
        success: () => {
          CTFd.fetch(`/api/v1/files/${fileId}`, {
            method: "DELETE"
          })
            .then(response => {
              return response.json();
            })
            .then(response => {
              if (response.success) {
                this.loadFiles();
              }
            });
        }
      });
    }
  },
  created() {
    this.loadFiles();
  }
};
</script>

<style scoped></style>
