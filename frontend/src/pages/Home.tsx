import { ArrowRight, BookOpen, MessageSquare, FileText, HelpCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          EU AI Act Assistant
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Your intelligent guide to understanding the EU AI Act regulations and compliance requirements.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gray-50 p-6 rounded-lg">
            <BookOpen className="w-8 h-8 text-blue-600 mb-4 mx-auto" />
            <h3 className="text-xl font-semibold mb-2">Ask Questions</h3>
            <p className="text-gray-600 mb-4">Get instant answers about EU AI Act regulations</p>
            <Link
              to="/qa"
              className="inline-flex items-center text-blue-600 hover:text-blue-800"
            >
              Start Asking <ArrowRight className="ml-2 w-4 h-4" />
            </Link>
          </div>
          <div className="bg-gray-50 p-6 rounded-lg">
            <FileText className="w-8 h-8 text-blue-600 mb-4 mx-auto" />
            <h3 className="text-xl font-semibold mb-2">Documentation</h3>
            <p className="text-gray-600 mb-4">Access detailed EU AI Act documentation</p>
            <button className="inline-flex items-center text-blue-600 hover:text-blue-800">
              View Docs <ArrowRight className="ml-2 w-4 h-4" />
            </button>
          </div>
          <div className="bg-gray-50 p-6 rounded-lg">
            <HelpCircle className="w-8 h-8 text-blue-600 mb-4 mx-auto" />
            <h3 className="text-xl font-semibold mb-2">Compliance Guide</h3>
            <p className="text-gray-600 mb-4">Learn about compliance requirements</p>
            <button className="inline-flex items-center text-blue-600 hover:text-blue-800">
              Get Started <ArrowRight className="ml-2 w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <div className="mt-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Updates</h2>
        <div className="space-y-4">
          <div className="border-l-4 border-blue-500 pl-4">
            <h3 className="text-lg font-semibold text-gray-900">Latest EU AI Act Amendments</h3>
            <p className="text-gray-600">Stay informed about the latest changes to EU AI regulations.</p>
          </div>
          <div className="border-l-4 border-blue-500 pl-4">
            <h3 className="text-lg font-semibold text-gray-900">Compliance Deadlines</h3>
            <p className="text-gray-600">Important dates and deadlines for EU AI Act compliance.</p>
          </div>
          <div className="border-l-4 border-blue-500 pl-4">
            <h3 className="text-lg font-semibold text-gray-900">Implementation Guidelines</h3>
            <p className="text-gray-600">Detailed guidelines for implementing EU AI Act requirements.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home; 