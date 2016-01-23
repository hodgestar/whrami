module.exports = function (grunt) {
  grunt.loadNpmTasks('grunt-bower-task');

  grunt.initConfig({
    bower: {
      install: {
        options: {
          layout: 'byComponent',
          cleanTargetDir: true,
          targetDir: 'whrami/static/vendor'
        }
      }
    },
  });

  grunt.registerTask('default', [
    'bower'
  ]);

};
