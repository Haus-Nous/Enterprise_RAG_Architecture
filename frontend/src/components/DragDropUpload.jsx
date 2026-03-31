import React, { useState, useCallback } from 'react';
import { UploadCloud, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import './DragDropUpload.css';

const DragDropUpload = ({ onUploadSuccess }) => {
    const [isDragging, setIsDragging] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [status, setStatus] = useState(null); // { type: 'success' | 'error', message: string }

    const handleDragOver = useCallback((e) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e) => {
        e.preventDefault();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback(async (e) => {
        e.preventDefault();
        setIsDragging(false);

        const file = e.dataTransfer?.files[0];
        if (!file) return;

        await uploadFile(file);
    }, []);

    const handleFileInput = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        await uploadFile(file);
    };

    const uploadFile = async (file) => {
        const validTypes = ['application/pdf', 'text/markdown'];
        const validExtensions = ['.pdf', '.md'];

        const isExtensionValid = validExtensions.some(ext => file.name.toLowerCase().endsWith(ext));

        if (!validTypes.includes(file.type) && !isExtensionValid) {
            setStatus({ type: 'error', message: 'Only .pdf and .md files are supported.' });
            return;
        }

        setUploading(true);
        setStatus(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8000/api/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Upload failed on server.');
            }

            setStatus({ type: 'success', message: `${file.name} uploaded!` });

            // Tell parent component to trigger a re-index
            if (onUploadSuccess) {
                onUploadSuccess();
            }

            // Clear success message after 3 seconds
            setTimeout(() => {
                setStatus(null);
            }, 3000);

        } catch (err) {
            console.error('Error uploading file:', err);
            setStatus({ type: 'error', message: 'Failed to upload document.' });
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="upload-container">
            <div
                className={`drop-zone ${isDragging ? 'dragging' : ''} ${uploading ? 'uploading' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => document.getElementById('fileUpload').click()}
            >
                <input
                    type="file"
                    id="fileUpload"
                    className="file-input-hidden"
                    accept=".pdf,.md"
                    onChange={handleFileInput}
                />

                {uploading ? (
                    <div className="upload-state uploading">
                        <div className="spinner"></div>
                        <p>Uploading to Database...</p>
                    </div>
                ) : status?.type === 'success' ? (
                    <div className="upload-state success">
                        <CheckCircle size={24} />
                        <p>{status.message}</p>
                    </div>
                ) : (
                    <div className="upload-state idle">
                        <UploadCloud size={24} className="upload-icon" />
                        <p className="upload-text">Click or drag a <b>PDF</b> / <b>MD</b> file here</p>
                    </div>
                )}
            </div>

            {status?.type === 'error' && (
                <div className="upload-error">
                    <AlertCircle size={12} />
                    <span>{status.message}</span>
                </div>
            )}
        </div>
    );
};

export default DragDropUpload;
