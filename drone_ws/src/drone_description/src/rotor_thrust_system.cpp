#include <gz/sim/System.hh> // Provides the base Gazebo system and simulation updates
#include <gz/sim/Model.hh> // Allows work on a Gazebo model
#include <gz/sim/Link.hh> // Allows forces to be applied to specific links
#include <gz/sim/components/AngularVelocity.hh> // Gives access to link's angular velocity
#include <gz/sim/components/Link.hh> // Provides link components
#include <gz/plugin/Register.hh> // Allows registration of this class as a gazebo plugin
#include <gz/sim/components/Name.hh>
#include <gz/sim/components/Model.hh>
#include <gz/common/Console.hh>

#include <cmath>
#include <vector>
#include <iostream>
#include <string>
#include <yaml-cpp/yaml.h>

namespace rotor_thrust{ // a way of grouping c++ code under a name
    class RotorThrustSystem : public gz::sim::System, public gz::sim::ISystemPreUpdate{ // Inherits the ISystemPreUpdate to tell Gazebo we want the PreUpdate fucntion to be called
    private:
        bool initialised{false};
        double kF{0.0};
        gz::sim::Model model{gz::sim::kNullEntity};
        // All variables are initialised to essentially zero
        std::vector<std::string> rotors{"spinner_link","spinner_link_1","spinner_link_2","spinner_link_3"};
    public:
        void PreUpdate(const gz::sim::UpdateInfo&, gz::sim::EntityComponentManager& ecm) override{
            gzmsg << "ROTOR THRUST PLUGIN RUNNING" << std::endl;
            // UpdateInfo for gaining information about the current simulation step
            // EntityComponentManager for accessing and modifying entities and their components
            if(!initialised){
                model  = gz::sim::Model(
                    ecm.EntityByComponents(
                        gz::sim::components::Model(),
                        gz::sim::components::Name("quadcopter")
                    )
                );
                // Searching for a model to gain its type and name
                // Once initalised this prevents us for entering this if statement
                
                try{
                    std::string yaml_filename{"/home/unknown/Main_Folder/Github/ROS-2/drone_ws/src/drone_controllers/config/mellinger_controller.yaml"};
                    YAML::Node config = YAML::LoadFile(yaml_filename);
                    kF = config["mellinger_controller"]["ros__parameters"]["kF"].as<double>();
                }
                catch(const YAML::Exception& e){
                    std::cerr << "Error parsing YAML: " << e.what() << std::endl;
                    return;
            
                }
                // For getting the kF from the parameter yaml file
                initialised = true;
            }
            
            
            for(const auto& rotor: rotors){
            // For looping through the motors in the vector
                auto linkEntity = model.LinkByName(ecm, rotor);
                // link is found and initalised to a variable
                if(linkEntity == gz::sim::kNullEntity) continue;
                // kNullEntity means Gazebo did not find the link
                gz::sim::Link link(linkEntity);
                // Creating a link object
                auto angularVel = ecm.Component<gz::sim::components::AngularVelocity>(linkEntity);
                // Extracting the angular components from link
                if(!angularVel) continue;
                // If there are none this would return false and onto the next iteration
                double omega = angularVel->Data().Z();
                // Extracting the angular velocity around the z axis
                double thrust = kF * omega * omega;
                gzmsg << rotor << ": " << "Entity= " << linkEntity << "Omega= " << omega << "Thrust= " << thrust << std::endl;
                // Aquiring the thrust
                link.AddWorldForce(ecm, gz::math::Vector3d(0,0,thrust));
                // Applying the thrust to the z axis
            }
            
            
        }
    };
}

GZ_ADD_PLUGIN(
    rotor_thrust::RotorThrustSystem,
    gz::sim::System,
    gz::sim::ISystemPreUpdate
)
// This tells gazebo that RotorThrustSystem is an actual plugin