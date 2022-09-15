project(MainWidget VERSION 1.0.0)

include_directories(./include)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_PREFIX_PATH /opt/homebrew/Cellar/qt/6.3.1_1)

SET(EXECUTABLE_OUTPUT_PATH ${DockerAutoBuild_SOURCE_DIR}/bin)


find_package(Qt6 COMPONENTS
        Core
        Gui
        Widgets
        REQUIRED)


file(GLOB HEADER_LIST include/*.h)
file(GLOB UI_LIST form/*.ui)

aux_source_directory(./ SRC_LIST)

add_executable(${PROJECT_NAME} ${SRC_LIST} ${HEADER_LIST} ${UI_LIST})


target_link_libraries(${PROJECT_NAME} PUBLIC
        Qt::Core
        Qt::Gui
        Qt::Widgets
        )

