file(GLOB panoc_SRC
    "*.c"
)
add_library(PANOC_lib STATIC ${panoc_SRC})
set_property(TARGET PANOC_lib PROPERTY C_STANDARD 90)

# this is nessesary for the python interface, and doesnt really matter for the tests
set_property(TARGET PANOC_lib PROPERTY POSITION_INDEPENDENT_CODE ON)