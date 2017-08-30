file(GLOB panoc_SRC
    "*.c"
)
add_library(PANOC_lib STATIC ${panoc_SRC})