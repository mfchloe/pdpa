import { useState } from "react";

export default function App() {
  const [query, setQuery] = useState("");
  const [summary, setSummary] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [results] = useState([
    {
      section: "PDPA Sec 26D",
      text: "Notification required for data breaches affecting 500 or more individuals must be made to the Commission within 72 hours of discovery. The notification must include details of the breach, affected data, and remedial measures taken.",
      source: "PDPA PDF",
      page: 12,
    },
    {
      section: "Schedule 1",
      text: "Consent is deemed given when an individual voluntarily provides personal data for a purpose that a reasonable person would consider appropriate in the circumstances, and the individual has been notified of the purpose.",
      source: "PDPA PDF",
      page: 3,
    },
    {
      section: "PDPA Sec 13",
      text: "Organizations must implement appropriate security arrangements to protect personal data in their possession or under their control against unauthorized access, collection, use, disclosure, copying, modification, disposal or similar risks.",
      source: "PDPA PDF",
      page: 8,
    },
  ]);

  const handleSubmit = async () => {
    if (!query.trim()) return;

    setIsLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      setSummary(data.answer);
    } catch (err) {
      console.error(err);
      setSummary(
        "Sorry, there was an error processing your request. Please try again."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && e.ctrlKey) {
      handleSubmit();
    }
  };

  const styles = {
    container: {
      minHeight: "100vh",
      background: "linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%)",
      fontFamily:
        '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    },
    mainLayout: {
      display: "flex",
      height: "100vh",
    },
    leftPanel: {
      width: "50%",
      padding: "32px",
      display: "flex",
      flexDirection: "column",
    },
    rightPanel: {
      width: "50%",
      padding: "32px",
      display: "flex",
      flexDirection: "column",
      borderLeft: "1px solid #e2e8f0",
    },
    header: {
      marginBottom: "32px",
    },
    headerTop: {
      display: "flex",
      alignItems: "center",
      gap: "12px",
      marginBottom: "8px",
    },
    iconContainer: {
      padding: "8px",
      backgroundColor: "#2563eb",
      color: "white",
      borderRadius: "8px",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    },
    title: {
      fontSize: "30px",
      fontWeight: "bold",
      color: "#1e293b",
      margin: 0,
    },
    subtitle: {
      color: "#64748b",
      margin: 0,
      fontSize: "16px",
    },
    inputSection: {
      flex: 1,
      display: "flex",
      flexDirection: "column",
      gap: "24px",
    },
    label: {
      display: "block",
      fontSize: "14px",
      fontWeight: "600",
      color: "#374151",
      marginBottom: "12px",
    },
    textareaContainer: {
      position: "relative",
    },
    textarea: {
      width: "100%",
      height: "256px",
      padding: "16px",
      border: "2px solid #e2e8f0",
      borderRadius: "12px",
      resize: "none",
      fontSize: "16px",
      lineHeight: "1.5",
      backgroundColor: "white",
      boxShadow: "0 1px 3px rgba(0, 0, 0, 0.1)",
      transition: "border-color 0.2s ease",
      outline: "none",
      fontFamily: "inherit",
    },
    textareaFocus: {
      borderColor: "#3b82f6",
    },
    keyboardHint: {
      position: "absolute",
      bottom: "12px",
      right: "12px",
      fontSize: "12px",
      color: "#9ca3af",
    },
    submitButton: {
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      gap: "8px",
      background: "linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)",
      color: "white",
      padding: "12px 24px",
      borderRadius: "12px",
      border: "none",
      fontWeight: "600",
      fontSize: "16px",
      cursor: "pointer",
      boxShadow: "0 4px 12px rgba(37, 99, 235, 0.4)",
      transition: "all 0.2s ease",
      fontFamily: "inherit",
    },
    submitButtonHover: {
      background: "linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%)",
      boxShadow: "0 6px 16px rgba(37, 99, 235, 0.5)",
      transform: "translateY(-1px)",
    },
    submitButtonDisabled: {
      opacity: "0.5",
      cursor: "not-allowed",
      transform: "none",
      boxShadow: "0 2px 8px rgba(37, 99, 235, 0.2)",
    },
    spinner: {
      width: "20px",
      height: "20px",
      border: "2px solid white",
      borderTop: "2px solid transparent",
      borderRadius: "50%",
      animation: "spin 1s linear infinite",
    },
    summaryCard: {
      backgroundColor: "white",
      borderRadius: "12px",
      boxShadow: "0 1px 3px rgba(0, 0, 0, 0.1)",
      border: "1px solid #e2e8f0",
      overflow: "hidden",
    },
    summaryHeader: {
      display: "flex",
      alignItems: "center",
      gap: "8px",
      padding: "12px 16px",
      background: "linear-gradient(135deg, #fdf4ff 0%, #fce7f3 100%)",
      borderBottom: "1px solid #e2e8f0",
    },
    summaryContent: {
      padding: "16px",
      height: "128px",
      overflowY: "auto",
      fontSize: "14px",
      lineHeight: "1.6",
      color: "#374151",
    },
    summaryPlaceholder: {
      color: "#9ca3af",
      fontStyle: "italic",
    },
    resultsHeader: {
      display: "flex",
      alignItems: "center",
      gap: "12px",
      marginBottom: "24px",
    },
    resultsTitle: {
      fontSize: "24px",
      fontWeight: "bold",
      color: "#1e293b",
      margin: 0,
    },
    resultsContainer: {
      flex: 1,
      overflow: "hidden",
    },
    resultsList: {
      height: "100%",
      overflowY: "auto",
      paddingRight: "8px",
    },
    resultCard: {
      backgroundColor: "white",
      borderRadius: "12px",
      boxShadow: "0 1px 3px rgba(0, 0, 0, 0.1)",
      border: "1px solid #e2e8f0",
      marginBottom: "16px",
      transition: "box-shadow 0.2s ease",
    },
    resultCardHover: {
      boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
    },
    resultHeader: {
      padding: "16px 20px",
      background: "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
      borderBottom: "1px solid #e2e8f0",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
    },
    sectionTitle: {
      fontWeight: "bold",
      fontSize: "18px",
      color: "#1e293b",
      margin: 0,
    },
    resultMeta: {
      display: "flex",
      alignItems: "center",
      gap: "8px",
      fontSize: "14px",
      color: "#64748b",
    },
    sourceBadge: {
      padding: "4px 8px",
      backgroundColor: "#dbeafe",
      color: "#1d4ed8",
      borderRadius: "6px",
      fontWeight: "500",
      fontSize: "12px",
    },
    resultContent: {
      padding: "20px",
    },
    resultText: {
      color: "#374151",
      lineHeight: "1.6",
      marginBottom: "16px",
      margin: "0 0 16px 0",
    },
    viewButton: {
      display: "inline-flex",
      alignItems: "center",
      gap: "4px",
      color: "#2563eb",
      fontSize: "14px",
      fontWeight: "500",
      textDecoration: "none",
      cursor: "pointer",
      transition: "color 0.2s ease",
      border: "none",
      background: "none",
      padding: 0,
      fontFamily: "inherit",
    },
    viewButtonHover: {
      color: "#1d4ed8",
    },
    emptyState: {
      textAlign: "center",
      padding: "48px 12px",
    },
    emptyStateIcon: {
      width: "48px",
      height: "48px",
      color: "#cbd5e1",
      margin: "0 auto 16px",
    },
    emptyStateText: {
      color: "#64748b",
      margin: 0,
    },
  };

  return (
    <div style={styles.container}>
      <style jsx>{`
        @keyframes spin {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }

        .submit-button:hover:not(:disabled) {
          background: linear-gradient(
            135deg,
            #1d4ed8 0%,
            #1e40af 100%
          ) !important;
          box-shadow: 0 6px 16px rgba(37, 99, 235, 0.5) !important;
          transform: translateY(-1px) !important;
        }

        .result-card:hover {
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        }

        .view-button:hover {
          color: #1d4ed8 !important;
        }

        .textarea:focus {
          border-color: #3b82f6 !important;
        }
      `}</style>

      <div style={styles.mainLayout}>
        {/* Left Panel */}
        <div style={styles.leftPanel}>
          {/* Header */}
          <div style={styles.header}>
            <div style={styles.headerTop}>
              <div style={styles.iconContainer}>
                <svg
                  width="24"
                  height="24"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                  />
                </svg>
              </div>
              <h1 style={styles.title}>PDPA Statute Finder</h1>
            </div>
            <p style={styles.subtitle}>
              Describe your scenario to find relevant PDPA sections and get
              AI-powered insights
            </p>
          </div>

          {/* Query Input */}
          <div style={styles.inputSection}>
            <div style={styles.textareaContainer}>
              <label style={styles.label}>Describe Your Scenario</label>
              <textarea
                className="textarea"
                style={styles.textarea}
                placeholder="e.g., Our company experienced a data breach affecting customer email addresses and phone numbers. What are our notification obligations under PDPA?"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
              />
              <div style={styles.keyboardHint}>Ctrl+Enter to search</div>
            </div>

            <button
              className="submit-button"
              style={{
                ...styles.submitButton,
                ...(isLoading || !query.trim()
                  ? styles.submitButtonDisabled
                  : {}),
              }}
              onClick={handleSubmit}
              disabled={isLoading || !query.trim()}
            >
              {isLoading ? (
                <>
                  <div style={styles.spinner}></div>
                  Analyzing...
                </>
              ) : (
                <>
                  <svg
                    width="20"
                    height="20"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    />
                  </svg>
                  Find Relevant Sections
                </>
              )}
            </button>

            {/* LLM Summary */}
            <div style={styles.summaryCard}>
              <div style={styles.summaryHeader}>
                <svg
                  width="18"
                  height="18"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  style={{ color: "#9333ea" }}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
                  />
                </svg>
                <h2 style={{ fontWeight: "600", color: "#1e293b", margin: 0 }}>
                  AI Summary
                </h2>
              </div>
              <div style={styles.summaryContent}>
                {summary ? (
                  <p style={styles.resultText}>{summary}</p>
                ) : (
                  <p style={styles.summaryPlaceholder}>
                    AI summary will appear here after you submit a query...
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Right Panel */}
        <div style={styles.rightPanel}>
          <div style={styles.resultsHeader}>
            <svg
              width="24"
              height="24"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              style={{ color: "#64748b" }}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <h2 style={styles.resultsTitle}>Relevant Sections</h2>
          </div>

          <div style={styles.resultsContainer}>
            <div style={styles.resultsList}>
              {results.map((item, idx) => (
                <div
                  key={idx}
                  className="result-card"
                  style={styles.resultCard}
                >
                  {/* Section Header */}
                  <div style={styles.resultHeader}>
                    <h3 style={styles.sectionTitle}>{item.section}</h3>
                    <div style={styles.resultMeta}>
                      <span style={styles.sourceBadge}>{item.source}</span>
                      <span style={{ color: "#cbd5e1" }}>•</span>
                      <span>Page {item.page}</span>
                    </div>
                  </div>

                  {/* Content */}
                  <div style={styles.resultContent}>
                    <p style={styles.resultText}>{item.text}</p>

                    {/* Action Button */}
                    <button className="view-button" style={styles.viewButton}>
                      <svg
                        width="14"
                        height="14"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                        />
                      </svg>
                      View Full Section
                    </button>
                  </div>
                </div>
              ))}

              {/* Empty State */}
              {results.length === 0 && (
                <div style={styles.emptyState}>
                  <svg
                    style={styles.emptyStateIcon}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  <p style={styles.emptyStateText}>
                    No results yet. Submit a query to see relevant PDPA
                    sections.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
