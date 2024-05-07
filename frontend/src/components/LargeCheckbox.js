import React from 'react';
import './LargeCheckbox.css'; // Assuming CSS is imported

function LargeCheckbox({ checked, onChange }) {
  return (
    <div className={`large-checkbox ${checked ? 'checked' : 'unchecked'}`} onClick={onChange}>
      <i className="fas fa-check"></i> {/* Always show the checkmark */}
    </div>
  );
}

export default LargeCheckbox;