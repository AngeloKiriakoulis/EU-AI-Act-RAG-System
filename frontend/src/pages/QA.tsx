import { useState } from 'react';
import { MessageSquare, Loader2 } from 'lucide-react';
import { API_BASE_URL } from '../config';

interface QAResponse {
  answer: string;
  chunks: Array<{
    text: string;
    metadata: any;
    distance: number;
  }>;
}

const QA = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setAnswer('');

    try {
      console.log('Sending request to backend...');
      const response = await fetch(`${API_BASE_URL}/api/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ text: question }),
      });

      console.log('Response status:', response.status);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data: QAResponse = await response.json();
      console.log('Received response:', data);
      setAnswer(data.answer);
    } catch (err) {
      console.error('Error details:', err);
      setError(err instanceof Error ? err.message : 'Failed to get answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <div className="flex items-center">
            <MessageSquare className="w-6 h-6 text-gray-500 mr-2" />
            <h2 className="text-2xl font-bold text-gray-900">EU AI Act Q&A</h2>
          </div>
        </div>
        <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="question" className="block text-sm font-medium text-gray-700">
                Your Question
              </label>
              <div className="mt-1">
                <textarea
                  id="question"
                  name="question"
                  rows={4}
                  className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="Ask a question about the EU AI Act..."
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                />
              </div>
            </div>

            {error && (
              <div className="text-red-600 text-sm">{error}</div>
            )}

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={loading || !question.trim()}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <Loader2 className="animate-spin -ml-1 mr-2 h-4 w-4" />
                    Getting Answer...
                  </>
                ) : (
                  'Ask Question'
                )}
              </button>
            </div>
          </form>

          {answer && (
            <div className="mt-8">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Answer</h3>
              <div className="prose max-w-none">
                <p className="text-gray-700 whitespace-pre-wrap">{answer}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default QA; 