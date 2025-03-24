import { Link } from 'react-router-dom';
import { Home, Settings, Users, MessageSquare } from 'lucide-react';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <Link to="/" className="text-xl font-bold text-gray-800">
                EU App
              </Link>
            </div>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              <Link
                to="/"
                className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900"
              >
                <Home className="w-4 h-4 mr-1" />
                Home
              </Link>
              <Link
                to="/qa"
                className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
              >
                <MessageSquare className="w-4 h-4 mr-1" />
                Q&A
              </Link>
              <Link
                to="/users"
                className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
              >
                <Users className="w-4 h-4 mr-1" />
                Users
              </Link>
              <Link
                to="/settings"
                className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
              >
                <Settings className="w-4 h-4 mr-1" />
                Settings
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 