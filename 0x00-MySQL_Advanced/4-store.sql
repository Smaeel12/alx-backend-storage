-- SQL script that creates a trigger that decreases the quantity of an item after adding a new order
-- Drop the existing trigger if it exists to avoid duplication
DROP TRIGGER IF EXISTS decrease_item_quantity;

-- Create the trigger to decrease item quantity after a new order is inserted
CREATE TRIGGER decrease_item_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Update the quantity of the item in the items table based on the new order
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;

