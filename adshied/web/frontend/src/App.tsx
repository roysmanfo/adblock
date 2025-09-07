import { useEffect, useState } from 'react';
import './style/dashboard.css';

function App() {
  const [blocked, setBlocked] = useState('');
  const [total, setTotal] = useState('');
  const [unique, setUnique] = useState('');

  const topBlockedDomains = [
    { name: 'ads.com', count: Math.round(Math.random() * 100) },
    { name: 'analytics.org', count: Math.round(Math.random() * 100) },
    { name: 'getstatus.example.it', count: Math.round(Math.random() * 100) },
    { name: 'cdn.ads.com', count: Math.round(Math.random() * 100) },
  ];

  function animateCounter(func: (value: string) => void, target = 0, duration = 2000) {
    const start = performance.now();

    function update(timestamp: number) {
      const progress = Math.min((timestamp - start) / duration, 1);
      const value = Math.floor(progress * target);
      func(value.toLocaleString()); // optional: adds commas for large numbers

      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        func(target.toLocaleString()); // ensure it ends cleanly
      }
    }

    requestAnimationFrame(update);
  }
  useEffect(() => {
    animateCounter(setBlocked, Math.round(Math.random() * 100));
    animateCounter(setTotal, Math.round(Math.random() * 50000));
    animateCounter(setUnique, Math.round(Math.random() * 100));
  }, []);

  return (
    <>
      <nav>
        <div className="logo">
          <i className="bi bi-shield-shaded"></i>
          AdShield
        </div>
        <div className="paths">
          <a href="/">
            <i className="bi bi-layout-wtf"></i>
            <div>Dashboard</div>
          </a>
          <a href="/logs">
            <i className="bi bi-file-earmark-text-fill"></i>
            <div>Logs</div>
          </a>
          <a href="/settings">
            <i className="bi bi-gear-fill"></i>
            <div>Settings</div>
          </a>
        </div>
      </nav>

      <main>
        <section className="stats">
          <div className="stat-item">
            <h2>{blocked}</h2>
            <p>Blocked Requests</p>
          </div>
          <div className="stat-item">
            <h2>{total}</h2>
            <p>Total Requests</p>
          </div>
          <div className="stat-item">
            <h2>{unique}</h2>
            <p>Unique Domains</p>
          </div>
        </section>
        <section className="top-blocked-domains">
          <h1>Most Blocked Domains</h1>
          <div className="table">
            <h4>Domain</h4>
            <h4>Blocked Requests</h4>

            {topBlockedDomains.map((d) => (
              <>
                <p>{d['name']}</p>
                <p>{d['count']}</p>
              </>
            ))}
          </div>
        </section>
      </main>
    </>
  );
}

export default App;
