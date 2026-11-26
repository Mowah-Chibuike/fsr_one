#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <geometry_msgs/msg/twist_stamped.hpp>

using std::placeholders::_1;

class TwistRelay: public rclcpp::Node
{
public:
    TwistRelay() : Node("twist_relay") {
        diff_controller_pub_ = this->create_publisher<geometry_msgs::msg::TwistStamped>("/diffbot_base_controller/cmd_vel", 10);
        diff_controller_sub_ = this->create_subscription<geometry_msgs::msg::Twist>("/diffbot_base_controller/cmd_vel_unstamped", 10, std::bind(&TwistRelay::diff_controller_cb, this, _1));

        key_sub_ = this->create_subscription<geometry_msgs::msg::TwistStamped>("/input_key/cmd_vel_stamped", 10, std::bind(&TwistRelay::key_sub_cb_, this, _1));

        key_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("/input_key/cmd_vel", 10);

        RCLCPP_INFO(this->get_logger(), "TwistRelay Initialized");
    }

private:
    rclcpp::Publisher<geometry_msgs::msg::TwistStamped>::SharedPtr diff_controller_pub_;
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr diff_controller_sub_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr key_pub_;
    rclcpp::Subscription<geometry_msgs::msg::TwistStamped>::SharedPtr key_sub_;

    void diff_controller_cb(geometry_msgs::msg::Twist::UniquePtr msg)
    {
        auto message = geometry_msgs::msg::TwistStamped();
        message.header.stamp = get_clock()->now();
        message.twist = *msg;
        diff_controller_pub_->publish(message);
    }

    void key_sub_cb_(geometry_msgs::msg::TwistStamped::UniquePtr msg)
    {
        auto message = geometry_msgs::msg::Twist();
        message = msg->twist;
        key_pub_->publish(message);
    }
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<TwistRelay>();

    rclcpp::spin(node);
    rclcpp::shutdown();

    return (0);
}