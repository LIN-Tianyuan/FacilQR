import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function QRCodeGenerator() {
    const [clientName, setClientName] = useState('');
    const [quantity, setQuantity] = useState(1);
    const [format, setFormat] = useState('PNG');
    const [color, setColor] = useState(false);
    const [borderRadius, setBorderRadius] = useState(false);
    const [logo, setLogo] = useState(null);
    const [server, setServer] = useState('prod');
    const [template, setTemplate] = useState('1');
    const [includeID, setIncludeID] = useState(false);
    const [beginID, setBeginID] = useState('');
    const [poweredByText, setPoweredByText] = useState('');
    const [loading, setLoading] = useState(false);
    const [quantityError, setQuantityError] = useState('');
    const [poweredByError, setPoweredByError] = useState('');

    const handleGenerate = () => {
        if (quantity < 1) {
            setQuantityError('Quantity must be at least 1');
            return;
        }
        setQuantityError('');

        setLoading(true);
        setTimeout(() => {
            alert('QR Code Generation Complete! 🎉');
            setLoading(false);
        }, 2000);
    };

    const handleQuantityBlur = () => {
        if (quantity < 1) {
            setQuantity(1);
            setQuantityError('Quantity must be at least 1');
        } else {
            setQuantityError('');
        }
    };

    const handlePoweredByBlur = () => {
        if (!/^[A-Za-z ]{1,9}$/.test(poweredByText)) {
            setPoweredByError('Must be 1-9 alphabetic characters only');
        } else {
            setPoweredByError('');
        }
    };

    return (
        <div className="container mt-5">
            <h2 className="text-center text-primary">QR Code Generator</h2>
            <div className="card p-4 shadow mt-4">
                <div className="mb-3">
                    <label className="form-label">Client Name</label>
                    <input type="text" className="form-control" value={clientName} onChange={(e) => setClientName(e.target.value)} required />
                </div>
                <div className="mb-3">
                    <label className="form-label">Quantity</label>
                    <input type="number" className="form-control" value={quantity} onChange={(e) => setQuantity(e.target.value)} onBlur={handleQuantityBlur} required />
                    {quantityError && <small className="text-danger">{quantityError}</small>}
                </div>
                <div className="mb-3">
                    <label className="form-label">Copyright Text (Powered By)</label>
                    <input type="text" className="form-control" maxLength="9" value={poweredByText} onChange={(e) => setPoweredByText(e.target.value.toUpperCase())} onBlur={handlePoweredByBlur} required />
                    {poweredByError && <small className="text-danger">{poweredByError}</small>}
                </div>
                <div className="mb-3">
                    <label className="form-label">Format</label>
                    <select className="form-select" value={format} onChange={(e) => setFormat(e.target.value)}>
                        <option value="PNG">PNG</option>
                        <option value="JPEG">JPEG</option>
                        <option value="PDF">PDF</option>
                    </select>
                </div>
                <div className="form-check mb-3">
                    <input className="form-check-input" type="checkbox" checked={color} onChange={() => setColor(!color)} />
                    <label className="form-check-label">Custom Color</label>
                </div>
                <div className="form-check mb-3">
                    <input className="form-check-input" type="checkbox" checked={borderRadius} onChange={() => setBorderRadius(!borderRadius)} />
                    <label className="form-check-label">Rounded Corners</label>
                </div>
                <div className="mb-3">
                    <label className="form-label">Upload Logo</label>
                    <input type="file" className="form-control" onChange={(e) => setLogo(e.target.files[0])} />
                </div>
                <div className="mb-3">
                    <label className="form-label">Server Environment</label>
                    <select className="form-select" value={server} onChange={(e) => setServer(e.target.value)}>
                        <option value="prod">Production</option>
                        <option value="pre-prod">Pre-Production</option>
                        <option value="re7">RE7</option>
                    </select>
                </div>
                <div className="mb-3">
                    <label className="form-label">QR Code Template</label>
                    <select className="form-select" value={template} onChange={(e) => setTemplate(e.target.value)}>
                        <option value="1">Classic</option>
                        <option value="2">Vertical (With Logo)</option>
                        <option value="3">Split (With Logo)</option>
                        <option value="4">Half Split (With Logo)</option>
                    </select>
                </div>
                {(template === '3' || template === '4') && (
                    <div className="mb-3">
                        <label className="form-label">Include ID</label>
                        <div className="form-check">
                            <input className="form-check-input" type="checkbox" checked={includeID} onChange={() => setIncludeID(!includeID)} />
                            <label className="form-check-label">Yes</label>
                        </div>
                        {includeID && (
                            <input type="text" className="form-control mt-2" placeholder="Enter Start ID" value={beginID} onChange={(e) => setBeginID(e.target.value)} />
                        )}
                    </div>
                )}
                <button className="btn btn-primary w-100" onClick={handleGenerate} disabled={loading}>
                    {loading ? 'Generating...' : 'Generate QR Code'}
                </button>
            </div>
        </div>
    );
}
