#include <SFML/Graphics.hpp>
#include <cmath>

int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "SFML Circle");

    sf::CircleShape circle(50);
    circle.setFillColor(sf::Color::Green);
    circle.setPosition(400, 100);

    // Variables for gravity and velocity
    float gravity = 0.005f; //0.2f
    sf::Vector2f velocity(0, 0);
    const float initialThrowVelocity = 0.4f;

    bool gameStarted = false;

    // Start screen text
    sf::Font font;
    if (!font.loadFromFile("arial.ttf")) {
        // Handle font loading error
        return 1;
    }
    sf::Text startText("Press SPACE to start", font, 30);
    startText.setFillColor(sf::Color::White);
    startText.setPosition(250, 250);

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            } else if (event.type == sf::Event::KeyPressed) {
                if (event.key.code == sf::Keyboard::Space) {
                    gameStarted = true;
                }
            }
        }

        if (!gameStarted) {
            window.clear();
            window.draw(startText);
            window.display();
            continue;  // Skip the rest of the loop until the game starts
        }

        // Update velocity with gravity
        velocity.y += gravity;

        // Update position based on velocity
        circle.move(velocity);

        // Handle collisions with walls
        if (circle.getPosition().y + circle.getRadius() * 2 >= window.getSize().y) {
            circle.setPosition(circle.getPosition().x, window.getSize().y - circle.getRadius() * 2);
            velocity.y = -velocity.y * 0.8f;  // Reverse direction and reduce velocity on bounce
        }
        if (circle.getPosition().y <= 0) {
            circle.setPosition(circle.getPosition().x, 0);
            velocity.y = -velocity.y * 0.8f;
        }
        if (circle.getPosition().x + circle.getRadius() * 2 >= window.getSize().x) {
            circle.setPosition(window.getSize().x - circle.getRadius() * 2, circle.getPosition().y);
            velocity.x = -velocity.x * 0.8f;
        }
        if (circle.getPosition().x <= 0) {
            circle.setPosition(0, circle.getPosition().y);
            velocity.x = -velocity.x * 0.8f;
        }

        // raycaster
        if (sf::Mouse::isButtonPressed(sf::Mouse::Left)) {
            sf::Vector2i mousePosition = sf::Mouse::getPosition(window);
            if (mousePosition.x >= circle.getPosition().x && mousePosition.x <= circle.getPosition().x + circle.getRadius() * 2 &&
                mousePosition.y >= circle.getPosition().y && mousePosition.y <= circle.getPosition().y + circle.getRadius() * 2) {
                sf::Vector2f throwDirection = sf::Vector2f(mousePosition.x - circle.getPosition().x - circle.getRadius(),
                                                           mousePosition.y - circle.getPosition().y - circle.getRadius());
                float throwMagnitude = std::sqrt(throwDirection.x * throwDirection.x + throwDirection.y * throwDirection.y);
                velocity = (throwDirection / throwMagnitude) * initialThrowVelocity;
            }
        }

        window.clear();
        window.draw(circle);
        window.display();
    }

    return 0;
}
