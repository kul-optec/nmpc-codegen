file(GLOB panoc_SRC
    "*.c"
)
add_library(PANOC_lib STATIC ${panoc_SRC})
set_property(TARGET PANOC_lib PROPERTY C_STANDARD 90)