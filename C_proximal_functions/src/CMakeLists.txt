file(GLOB PROXIMAL_FUNCTIONS_SRC
    "*.c"
)
file(GLOB PROXIMAL_FUNCTIONS_INTERNALS_SRC
    "internal_lib/*.c"
)

add_library(proximal_functions_lib STATIC ${PROXIMAL_FUNCTIONS_SRC} ${PROXIMAL_FUNCTIONS_INTERNALS_SRC})
set_property(TARGET proximal_functions_lib PROPERTY C_STANDARD 90)