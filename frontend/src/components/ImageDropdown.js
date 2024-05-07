import React, { useState, useEffect } from 'react';
import { Dropdown, Image } from 'react-bootstrap';

function ImageDropdown({ options, onChange, initialSelectedImage }) {
  const [selectedImage, setSelectedImage] = useState('');

  useEffect(() => {
    if (initialSelectedImage) {
      setSelectedImage(initialSelectedImage);
    }
  }, [initialSelectedImage]);

  const handleSelect = (value, imgSrc) => {
    setSelectedImage(imgSrc);
    onChange(value);
  };

  return (
    <Dropdown className="image-dropdown-select">
      <Dropdown.Toggle variant="white" id="dropdown-basic">
        {selectedImage ? (
          <Image src={selectedImage} alt="Selected" style={{ width: '50px', height: '50px' }} rounded />
        ) : 'Select Image'}
      </Dropdown.Toggle>

      <Dropdown.Menu className="image-dropdown-grid">
        {options.map(option => (
          <Dropdown.Item key={option.value} onClick={() => handleSelect(option.value, option.imgSrc)} className="d-inline-block">
            <Image src={option.imgSrc} alt="" style={{ width: '50px', height: '50px' }} />
          </Dropdown.Item>
        ))}
      </Dropdown.Menu>
    </Dropdown>
  );
}

export default ImageDropdown;
