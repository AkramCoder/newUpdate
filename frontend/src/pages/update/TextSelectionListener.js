import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { API_URL } from '../../constants';

function TextSelectionListener() {
    const [selectedText, setSelectedText] = useState('');
    const [showMessage, setShowMessage] = useState(false);
    const [message, setMessage] = useState('');
    const [messagePosition, setMessagePosition] = useState({ top: 0, left: 0 });

    const getStringType = async (text) => {
      await axios({
        method: 'POST',
        url: `${API_URL}user/process-text/`, 
        data: {input_text: text},
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(response => {
          console.log(response.data)
      }).catch(error => {
          console.log(error)
      })
    }

  useEffect(() => {
    function handleTextSelection() {
        const text = window.getSelection().toString();
        if (text) {
            const selection = window.getSelection();
            if (selection.rangeCount > 0) {
              const range = selection.getRangeAt(0);
              const rect = range.getBoundingClientRect();

              console.log(text)
              setSelectedText(text);
              setShowMessage(true);
              setMessage('This is a custom message.');
              
              getStringType(text)
              setMessagePosition({
                top: rect.bottom + window.scrollY - 50,
                left: rect.left + window.scrollX - 190,
              });
            }
          } else {
            setSelectedText('');
            setShowMessage(false);
            setMessage('');
          }
    }

    document.addEventListener("mouseup", handleTextSelection);

    return () => {
      document.removeEventListener("mouseup", handleTextSelection);
    };
  }, []);

  const messageStyle = {
    position: 'absolute',
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    border: '1px solid #ccc',
    borderRadius: '4px',
    padding: '4px',
    boxShadow: '0px 2px 5px rgba(0, 0, 0, 0.2)',
    display: showMessage ? 'block' : 'none',
    top: `${messagePosition.top}px`,
    left: `${messagePosition.left}px`,
  };

  return (
    <div>
      <div style={messageStyle}>
        {message}
      </div>
    </div>
  );
}

export default TextSelectionListener;
