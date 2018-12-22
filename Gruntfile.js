module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        config: {
            app: 'app'
        },

        connect: {
            options: {
                port: 9000,
                livereload: 35729,
                // Change this to '0.0.0.0' to access the server from outside
                hostname: 'localhost'
            },
            livereload: {
                options: {
                    open: true,
                    base: [
                        '.tmp',
                        '<%= config.app %>/public'
                    ]
                }
            },
        },
        watch: {
            options: {
                livereload: true,
            },
            livereload: {
                options: {
                    livereload: '<%= connect.options.livereload %>'
                },
                files: [
                    '<%= config.app %>/public/{,*/}*.html',
                    '<%= config.app %>/public/css/{,*/}*.css',
                    '<%= config.app %>/public/images/{,*/}*',
                ]
            },
            compass: {
                files: ['**/*.{scss,sass}'],
                tasks: ['compass:dev']
            },
            jinja: {
                files: ['app/src/templates/**'],
                tasks: ['jinja:main']
            },
            copy: {
                files: ['app/src/images/*', 'app/src/fonts/*'],
                tasks: ['copy:main']
            },
            concat: {
                files: ['app/src/js/*'],
                tasks: ['concat:dev']
            },
            shell: {
                files: ['app/src/templates/posts/**'],
                tasks: ['shell:generate_post_list']
            }
        },
        compass: {
            dev: {
                options: {
                    sassDir: ['app/src/stylesheets'],
                    cssDir: ['app/public/css'],
                    environment: 'development'
                }
            },
            prod: {
                options: {
                    sassDir: ['app/src/stylesheets'],
                    cssDir: ['app/public/css'],
                    environment: 'production',
                    outputStyle: 'compressed'
                }
            },
        },
        jinja: {
            main: {
                options:{
                    templateDirs: ['app/src/templates'],
                    contextRoot: 'app/src/templates/context'
                },
                files: [{
                    expand: true,
                    cwd: 'app/src/templates',
                    src: ['index.html', 'post_list.html', 'post_list_template.html', 'traduccio.html', 'posts/*.html'],
                    dest: 'app/public',
                    ext: '.html'
                }]
            }
        },
        copy: {
            main: {
                files: [
                    {
                        expand: true,
                        cwd: 'app/src/images',
                        src: '**/*',
                        dest: 'app/public/images/'
                    },
                    {
                        expand: true,
                        cwd: 'bower_components/fontawesome/webfonts/',
                        src: '**/*',
                        dest: 'app/public/webfonts/'
                    }
                ]

            }
        },
        concat: {
            dev: {
                src: [
                    'bower_components/jquery/dist/jquery.js',
                    'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
                    '/app/src/js/*.js'
                ],
                dest: 'app/public/js/main.js'
            },
            prod: {
                src: [
                    'bower_components/jquery/dist/jquery.js',
                    'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
                    'app/src/js/*.js'
                ],
                dest: 'app/public/js/main.js'
            }
        },
        shell: {
            generate_post_list: {
                options: {
                    stdout: true
                },
                command: 'python generate_post_list.py'
            }
        }
    });

    // Load the plugin
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-contrib-connect');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-jinja');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-shell');


    // Default task(s).
    grunt.registerTask('default', [
        'connect:livereload',
        'compass:dev',
        'concat:dev',
        'shell:generate_post_list',
        'jinja',
        'copy',
        'watch'
    ]);
    // prod build
    grunt.registerTask('prod', [
        'compass:prod',
        'shell:generate_post_list',
        'jinja',
        'concat:prod',
        'copy'
    ]);

};
