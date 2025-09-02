import './App.css';

function App() {
  return (
    <div className="sentinel-container">
      <header className="sentinel-header">
        /sentinel-logo.svg
        <h1 className="sentinel-title">SENTINEL</h1>
        <p className="sentinel-subtitle">Proactive OSINT Investigator</p>
      </header>

      <main className="sentinel-main">
        <section className="sentinel-section">
          <h2>Alerts</h2>
          <p>Structure fires and missing persons alerts will appear here.</p>
        </section>

        <section className="sentinel-section">
          <h2>Case Files</h2>
          <p>Manage and view active investigations.</p>
        </section>

        <section className="sentinel-section">
          <h2>OSINT Tools</h2>
          <p>Scraping, timelines, and pattern recognition tools.</p>
        </section>
      </main>
    </div>
  );
}

export default App;
