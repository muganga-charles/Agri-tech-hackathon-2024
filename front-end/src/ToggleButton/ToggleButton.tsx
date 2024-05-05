import React, { useState } from 'react';
import './ToggleButton.css'; // Import the CSS file for styling

interface ToggleButtonProps {
  onChange?: (isChecked: boolean) => void;
  defaultChecked?: boolean;
}

const ToggleButton: React.FC<ToggleButtonProps> = ({ onChange, defaultChecked }) => {
  const [checked, setChecked] = useState(defaultChecked || false);

  const handleClick = () => {
    const newState = !checked;
    setChecked(newState);
    if (onChange) {
      onChange(newState);
    }
  };

  return (
    <div className={`toggle-button ${checked ? 'checked' : ''}`} onClick={handleClick}>
      <div className="toggle-button-slider"></div>
    </div>
  );
};

export default ToggleButton;
